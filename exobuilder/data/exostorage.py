from pymongo import MongoClient
import pymongo

class EXOStorage(object):
    def __init__(self, conn_str, dbname='tmldb'):
        self.client = MongoClient(conn_str)
        self.db = self.client[dbname]

    def load_exo(self, exo_name):
        try:
            return self.db.exo_data.find({'name': exo_name}).next()
        except:
            return None

    def save_exo(self, exo_dict):
        exo_name = exo_dict['name']
        return self.db.exo_data.replace_one({'name': exo_name}, exo_dict, upsert=True)