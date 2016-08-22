from pymongo import MongoClient
import pymongo
import pickle

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