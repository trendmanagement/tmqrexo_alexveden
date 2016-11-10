from pymongo import MongoClient
import pymongo
import pickle
import re
import pandas as pd

class EXOStorage(object):
    def __init__(self, conn_str, dbname='tmldb'):
        self.client = MongoClient(conn_str)
        self.db = self.client[dbname]

    def load_series(self, exo_name):
        """
        Load EXO index series from MongoDB
        :param exo_name: name of EXO index
        :return: (tuple) series_df, exo_dic
        """
        try:
            data = self.db.exo_data.find({'name': exo_name}).next()

            # Loading metadata for EXO
            exo_dic = {'pcf': [], 'pcfqty': [], 'margin': 0, 'underlying': '', 'name': exo_name, 'dbdata': data}

            series_df = pickle.loads(data['series'])
            series_df.index = pd.to_datetime(series_df.index)

            return series_df, exo_dic
        except:
            return None, None


    def load_exo(self, exo_name):
        """
        Load EXO collection from Mongo (as is)
        :param exo_name:
        :return: EXO collection dict
        """
        try:
            return self.db.exo_data.find({'name': exo_name}).next()
        except:
            return None

    def save_exo(self, exo_dict):
        """
        Save EXO collections to MongoDB
        :param exo_dict: EXO collection dict
        :return: PyMondo.replace_one() result
        """
        exo_name = exo_dict['name']
        return self.db.exo_data.replace_one({'name': exo_name}, exo_dict, upsert=True)

    def exo_list(self, exo_filter='*', return_names=True):
        """
        Return EXO list stored in MongoDB
        :param exo_filter: '*' - include all, wildcard is allowed (like, 'ES_Bullish*')
        :param return_names: if True returns names list of EXO, otherwize returns MongoDB data collection list
        :return: list of EXO names
        """
        re_val = exo_filter.replace('*','.*')

        data = self.db.exo_data.find({'name': re.compile(re_val, re.IGNORECASE)})
        if return_names:
            return [exo['name'] for exo in data]
        else:
            return list(data)

    def swarms_info(self):
        """
        Aggregate swarm information by instrument, product, alpha type
        :return: dict of swarms information aggregation
        """
        return self.db['swarms'].aggregate(
            [
                {
                    '$group': {
                        '_id': None,
                        'instruments': {'$addToSet': '$instrument'},
                        'exo_types': {'$addToSet': '$exo_type'},
                        'alphas': {'$addToSet': '$alpha_name'},
                    }
                }
            ]
        ).next()

    def swarms_list(self, instruments_list=('*',), direction=(1, -1, 0), alpha_list=('*',), exo_list=('*',)):
        """
        Select swarms from Mongo using case INSENSITIVE filters (wildcards allowed)
        :param instruments_list: instruments list filter like '*', 'CL*', 'CL*9'
        :param direction: direction filter (1=Long, -1=Short, 0=Bidirectional)
        :param alpha_list: alpha name filter
        :param exo_list: exo list filter
        :return: Pandas.DataFrame(swarms_picked_equity), list(mongo_swarms_dicts)
        """
        def re_pattern(values_list, prepend='', append=''):
            result = ""
            for i,v in enumerate(values_list):
                re_val = v.replace('*', '.*')

                if i == 0:
                    result += '{0}({1}'.format(prepend, re_val)
                else:
                    result += '|{0}'.format(re_val)

            result += '){0}'.format(append)

            return re.compile(result, re.IGNORECASE)

        cursor = self.db['swarms'].find(
            {'$and':
                [
                    {'exo_name': re_pattern(instruments_list, prepend='^')},
                    {'exo_name': re_pattern(exo_list)},
                    {'direction': {'$in': direction}},
                    {'swarm_name': re_pattern(alpha_list)}
                ]
            }
        )

        swarm_data = []

        for swm in cursor:
            if 'picked_delta' in swm:
                swm['picked_delta'] = pickle.loads(swm['picked_delta'])
            if 'picked_equity' in swm:
                swm['picked_equity'] = pickle.loads(swm['picked_equity'])
            swarm_data.append(swm)

        series_dict = {}

        for s in swarm_data:
            series_dict[s['swarm_name']] = s['picked_equity']

        return pd.DataFrame(series_dict), swarm_data

    def swarms_positions(self, alpha_list=None):
        """
        Returns swarm positions with alpha_filter
        :param alpha_list: if None - select all, otherwize use list of alpha names ex. ['alpha1', 'alpha2']
        :return: dict {'alpha_name: {'exposure':..., 'exo_name':..., 'prev_exposure':...}
        """
        result = {}
        if alpha_list is not None:
            cursor = self.db['swarms'].find({'swarm_name': {'$in': list(alpha_list)}})
        else:
            cursor = self.db['swarms'].find()

        for c in cursor:
            result[c['swarm_name']] = {'exposure': c['last_exposure'], 'exo_name': c['exo_name'], 'prev_exposure': c['last_prev_exposure']}

        return result
