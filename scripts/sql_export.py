
import sys, argparse, logging
import pymssql
import _mssql
import datetime
from decimal import Decimal
import pymongo
from pymongo import MongoClient
from tqdm import tqdm, tnrange, tqdm_notebook

from scripts.settings import *


# SQL Server credentials
SQL_HOST = 'h9ggwlagd1.database.windows.net'
SQL_USER = 'modelread'
SQL_PASS = '4fSHRXwd4u'

sql_conn = pymssql.connect(SQL_HOST, SQL_USER + "@" + SQL_HOST, SQL_PASS, 'TMLDB')

def convert_dates(values):
    k,v = values
    if type(v) == datetime.date:
        return k, datetime.datetime.combine(
                v,
                datetime.datetime.min.time())
    if type(v) == Decimal:
        return k, float(v)
    if k == 'datetime' and type(v) == str:
        return k, datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
    else:
        return k, v



# Init mongo asset index
client = MongoClient('mongodb://admin:jsmHf598@10.0.1.2/admin?authMechanism=SCRAM-SHA-1')
mongo_db = client['tmldb_test']

# Storing futures
mongo_collection = mongo_db['tmp_bardata']
mongo_collection.create_index([('idbardata', pymongo.ASCENDING)], unique=True)
mongo_collection.create_index([('idcontract', pymongo.ASCENDING), ('datetime', pymongo.ASCENDING)], unique=True)

try:
    _bardata = mongo_collection.find({}).sort([('idbardata',-1)]).limit(1).next()
    print(_bardata)
    last_id = _bardata['idbardata']
except StopIteration:
    last_id = 0
print('Starting from idbardata: {0}'.format(last_id))

qry = 'SELECT * FROM cqgdb.tblbardata where idbardata > {0}'.format(last_id)
logging.debug(qry)

max_steps = 154521767
#pbar = tqdm_notebook(desc="Progress", total=max_steps)
pbar = tqdm(desc="Progress", total=max_steps)

c2 = sql_conn.cursor(as_dict=True)
c2.execute(qry)
for row in c2:
    data = dict(map(convert_dates, row.items()))
    #print(data)
    mongo_collection.insert_one(data)
    pbar.update(1)
    #break
pbar.close()

