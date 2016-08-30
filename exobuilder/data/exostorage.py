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
        try:
            data = self.db.exo_data.find({'name': exo_name}).next()

            # Loading metadata for EXO
            exo_dic = {'pcf': [], 'pcfqty': [], 'margin': 0, 'underlying': '', 'name': exo_name}

            return pickle.loads(data['series']), exo_dic
        except:
            return None, None


    def load_exo(self, exo_name):
        try:
            return self.db.exo_data.find({'name': exo_name}).next()
        except:
            return None

    def save_exo(self, exo_dict):
        exo_name = exo_dict['name']
        return self.db.exo_data.replace_one({'name': exo_name}, exo_dict, upsert=True)

    def exo_list(self, exo_filter='*'):

        re_val = exo_filter.replace('*','.*')

        data = self.db.exo_data.find({'name': re.compile(re_val, re.IGNORECASE)})
        return [exo['name'] for exo in data]

    def swarms_info(self):
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
                    {'alpha_name': re_pattern(alpha_list)}
                ]
            }
        )

        swarm_data = [swm for swm in cursor]

        series_dict = {}

        for s in swarm_data:
            series_dict[s['swarm_name']] = pickle.loads(s['picked_equity'])

        return pd.DataFrame(series_dict), swarm_data
