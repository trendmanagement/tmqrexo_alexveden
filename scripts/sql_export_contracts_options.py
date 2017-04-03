
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
SQL_USER = 'steve'
SQL_PASS = 'KYYAtv9P'

#SQL_HOST = 'h9ggwlagd1.database.windows.net'
#SQL_USER = 'modelread'
#SQL_PASS = '4fSHRXwd4u'

sql_conn = pymssql.connect(server=SQL_HOST, \
                           user=SQL_USER + "@" + SQL_HOST, password=SQL_PASS, database='TMLDB')

#sql_conn = pymssql.connect("h9ggwlagd1.database.windows.net", "modelread@h9ggwlagd1.database.windows.net", "4fSHRXwd4u", "TMLDB")

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
    elif k == 'expirationdate' and type(v) == str:
        return k, datetime.datetime.strptime(v, '%Y-%m-%d')
    elif k == 'spanoptionstart' and type(v) == str:
        return k, datetime.datetime.strptime(v, '%Y-%m-%d')
    elif k == 'optionstart' and type(v) == str:
        return k, datetime.datetime.strptime(v, '%Y-%m-%d')
    elif k == 'datastart' and type(v) == str:
        return k, datetime.datetime.strptime(v, '%Y-%m-%d')
    elif k == 'customdayboundarytime' and type(v) == str:
        return k, datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
    elif k == 'optioninputdatetime' and type(v) == str:
        return k, datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
    if k == 'date' and type(v) == str:
        return k, datetime.datetime.strptime(v, '%Y-%m-%d')
    else:
        return k, v

#MONGO_CONNSTR = 'mongodb://exowriter:qmWSy4K3@10.0.1.2/tmldb?authMechanism=SCRAM-SHA-1'
MONGO_CONNSTR = 'mongodb://tmqr:tmqr@10.0.1.2/tmldb_v2?authMechanism=SCRAM-SHA-1'
MONGO_CONNSTR_LOCAL = 'mongodb://localhost:27017'
MONGO_EXO_DB = 'tmldb_v2'
MONGO_EXO_DB_LOCAL = 'tmldb'

# Init mongo asset index
client = MongoClient(MONGO_CONNSTR)
mongo_db = client[MONGO_EXO_DB]

#mongo_collection.create_index([('idbardata', pymongo.ASCENDING)], unique=True)
#mongo_collection.create_index([('idcontract', pymongo.ASCENDING), ('datetime', pymongo.ASCENDING)], unique=True)
'''
print('contracts')
############################################################################
collection = mongo_db['contracts']

qry = 'SELECT * FROM cqgdb.tblcontracts '
logging.debug(qry)

max_steps = 1
pbar = tqdm(desc="Progress", total=max_steps)

c2 = sql_conn.cursor(as_dict=True)
c2.execute(qry)

cnt = 0
for row in c2:
    try:
        data = dict(map(convert_dates, row.items()))
        collection.replace_one({'idcontract':data['idcontract']},data,upsert=True)
        cnt += 1
    except TypeError:
        print('TypeError')
        print(row)
        break

    pbar.update(1)

print('Done {0} rows'.format(cnt))



print('options')
############################################################################
collection = mongo_db['options']

qry = 'SELECT * FROM cqgdb.tbloptions '
logging.debug(qry)

max_steps = 1
pbar = tqdm(desc="Progress", total=max_steps)

c2 = sql_conn.cursor(as_dict=True)
c2.execute(qry)

cnt = 0
for row in c2:
    try:
        data = dict(map(convert_dates, row.items()))
        collection.replace_one({'idoption':data['idoption']},data,upsert=True)
        cnt += 1
    except TypeError:
        print('TypeError')
        print(row)
        break

    pbar.update(1)

print('Done {0} rows'.format(cnt))

print('instruments')
############################################################################
collection = mongo_db['instruments']

qry = 'SELECT * FROM cqgdb.tblinstruments '
logging.debug(qry)

max_steps = 1
pbar = tqdm(desc="Progress", total=max_steps)

c2 = sql_conn.cursor(as_dict=True)
c2.execute(qry)

cnt = 0
for row in c2:
    try:
        data = dict(map(convert_dates, row.items()))
        collection.replace_one({'idinstrument':data['idinstrument']},data,upsert=True)
        cnt += 1
    except TypeError:
        print('TypeError')
        print(row)
        break

    pbar.update(1)

print('Done {0} rows'.format(cnt))


print('option_input_data')
############################################################################
collection = mongo_db['option_input_data']

qry = 'SELECT * FROM cqgdb.tbloptioninputdata '
logging.debug(qry)

max_steps = 1
pbar = tqdm(desc="Progress", total=max_steps)

c2 = sql_conn.cursor(as_dict=True)
c2.execute(qry)

cnt = 0
for row in c2:
    try:
        data = dict(map(convert_dates, row.items()))
        collection.replace_one({'idoptioninputsymbol':data['idoptioninputsymbol'],'optioninputdatetime':data['optioninputdatetime']},data,upsert=True)
        cnt += 1
    except TypeError:
        print('TypeError')
        print(row)
        break

    pbar.update(1)

print('Done {0} rows'.format(cnt))



print('futures_contract_settlements')
############################################################################

collection = mongo_db['futures_contract_settlements']

qry = 'SELECT * FROM cqgdb.tbldailycontractsettlements '
logging.debug(qry)

max_steps = 1
pbar = tqdm(desc="Progress", total=max_steps)

c2 = sql_conn.cursor(as_dict=True)
c2.execute(qry)

contract_settlements = []

cnt = 0
for row in c2:
    try:
        future_settlements = dict(map(convert_dates, row.items()));

        contract_settlements.append({'idcontract':future_settlements['idcontract'], \
                                     'date':future_settlements['date'], \
                                     'settlement':future_settlements['settlement'], \
                                     'volume':future_settlements['volume'],
                                     'openinterest':future_settlements['openinterest']})

        cnt += 1
    except TypeError:
        print('TypeError')
        print(row)
        break

    #if cnt > 3:
    #    break

    pbar.update(1)

#print(contract_settlements)

result  = collection.insert_many(contract_settlements)

#print(result.inserted_ids)

print('Done {0} rows'.format(cnt))


print('options data')
############################################################################
collection = mongo_db['options_data']

qry = 'SELECT * FROM cqgdb.tbloptiondata '
logging.debug(qry)

max_steps = 1
pbar = tqdm(desc="Progress", total=max_steps)

c2 = sql_conn.cursor(as_dict=True)
c2.execute(qry)

contract_settlements = []

cnt = 0
for row in c2:
    try:
        option_settlements = dict(map(convert_dates, row.items()));

        contract_settlements.append({'idoption': option_settlements['idoption'], \
                                     'datetime': option_settlements['datetime'], \
                                     'price': option_settlements['price'], \
                                     'impliedvol': option_settlements['impliedvol'], \
                                     'timetoexpinyears': option_settlements['timetoexpinyears']})

        if(cnt % 100000 == 0):
            if(len(contract_settlements) > 0):
                collection.insert_many(contract_settlements)

            contract_settlements = []

        cnt += 1
    except TypeError:
        print('TypeError')
        print(row)
        break

    #if cnt > 3:
    #    break

    pbar.update(1)

#print(contract_settlements)

if(len(contract_settlements) > 0):
    result  = collection.insert_many(contract_settlements)

#print(result.inserted_ids)

print('Done {0} rows'.format(cnt))



print('Bar data')
############################################################################
collection = mongo_db['contracts_bars']

collection.create_index([('idcontract',pymongo.ASCENDING),('datetime',pymongo.ASCENDING)])
collection.create_index([('idcontract',pymongo.ASCENDING),('datetime',pymongo.DESCENDING)])

qry = 'SELECT * FROM cqgdb.tblbardata '
logging.debug(qry)

max_steps = 1
pbar = tqdm(desc="Progress", total=max_steps)

c2 = sql_conn.cursor(as_dict=True)
c2.execute(qry)

contract_bars = []

cnt = 0
for row in c2:
    try:
        bar = dict(map(convert_dates, row.items()));

        contract_bars.append({'datetime': bar['datetime'], \
                                     'open': bar['open'], \
                                     'high': bar['high'], \
                                     'low': bar['low'], \
                                     'close': bar['close'], \
                              'idcontract': bar['idcontract'],
                              })

        if(cnt % 100000 == 0):
            if(len(contract_bars) > 0):
                collection.insert_many(contract_bars)

            contract_bars = []

        cnt += 1
    except TypeError:
        print('TypeError')
        print(row)
        break

    #if cnt > 3:
    #    break

    pbar.update(1)

#print(contract_settlements)

if(len(contract_bars) > 0):
    result  = collection.insert_many(contract_bars)

#print(result.inserted_ids)

print('Done {0} rows'.format(cnt))



print('Expiration data')
############################################################################
collection = mongo_db['contractexpirations']

collection.create_index([('optionyear',pymongo.ASCENDING),('optionmonthint',pymongo.ASCENDING),('contracttype',pymongo.ASCENDING)])

qry = 'SELECT * FROM cqgdb.tblcontractexpirations '
logging.debug(qry)

max_steps = 1
pbar = tqdm(desc="Progress", total=max_steps)

c2 = sql_conn.cursor(as_dict=True)
c2.execute(qry)

contract_bars = []

cnt = 0
for row in c2:
    try:
        bar = dict(map(convert_dates, row.items()));

        contract_description = 'future'
        if bar['contracttype'] == 2:
            contract_description = 'option'

        contract_bars.append({'contracttype': bar['contracttype'], \
                                     'contractdescription': contract_description, \
                                     'idinstrument': bar['idinstrument'], \
                                     'optionyear': bar['optionyear'], \
                                     'optionmonthint': bar['optionmonthint'], \
                              'expirationdate': bar['expirationdate']})

        if(cnt % 100000 == 0):
            if(len(contract_bars) > 0):
                collection.insert_many(contract_bars)

            contract_bars = []

        cnt += 1
    except TypeError:
        print('TypeError')
        print(row)
        break

    #if cnt > 3:
    #    break

    pbar.update(1)

#print(contract_settlements)

if(len(contract_bars) > 0):
    result  = collection.insert_many(contract_bars)

#print(result.inserted_ids)
'''
#print('Done {0} rows'.format(cnt))

print('Bar data')
############################################################################

max_steps = 6615
pbar = tqdm(desc="Progress", total=max_steps)

contracts_col = mongo_db['contracts']
contracts_mongo = contracts_col.find({})
contracts_dict = {}

for contract_mongo in contracts_mongo:
    tup = (contract_mongo['idinstrument'],contract_mongo['year'],contract_mongo['month'])
    contracts_dict[tup] = contract_mongo


contracts_qry = 'SELECT * FROM cqgdb.tblcontracts'
contracts_sql = sql_conn.cursor(as_dict=True)
contracts_sql.execute(contracts_qry)

sql_conn_2 = pymssql.connect(server=SQL_HOST, \
                           user=SQL_USER + "@" + SQL_HOST, password=SQL_PASS, database='TMLDB')

count = 0
for contract_row in contracts_sql:
    #print(contract_row)

    if (contract_row['idinstrument'],contract_row['year'],contract_row['month']) in contracts_dict:
        contract_mongo2 = contracts_dict[contract_row['idinstrument'],contract_row['year'],contract_row['month']]

        #print(contract_mongo2)

        contract_query_bar = 'SELECT datetime,volume FROM cqgdb.tblbardata WHERE idcontract = ' \
                             + str(contract_row['idcontract']) + ' ORDER BY datetime'
        c2 = sql_conn_2.cursor(as_dict=True)
        c2.execute(contract_query_bar)

        for row in c2:
            if row['volume'] > 0:
                rowdatetime = datetime.datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')

                test = mongo_db['contracts_bars'].update(
                    {'idcontract':contract_mongo2['idcontract'],'datetime':rowdatetime},
                    {'$set':{'volume':row['volume']}},upsert=False, multi=False)

                print(test)

    pbar.update(1)
    count+=1


'''
collection = mongo_db['contracts_bars']

collection.create_index([('idcontract',pymongo.ASCENDING),('datetime',pymongo.ASCENDING)])
collection.create_index([('idcontract',pymongo.ASCENDING),('datetime',pymongo.DESCENDING)])

qry = 'SELECT * FROM cqgdb.tblbardata '
logging.debug(qry)

max_steps = 1
pbar = tqdm(desc="Progress", total=max_steps)

c2 = sql_conn.cursor(as_dict=True)
c2.execute(qry)

contract_bars = []

cnt = 0
for row in c2:
    try:
        bar = dict(map(convert_dates, row.items()));

        contract_bars.append({'datetime': bar['datetime'], \
                                     'open': bar['open'], \
                                     'high': bar['high'], \
                                     'low': bar['low'], \
                                     'close': bar['close'], \
                              'idcontract': bar['idcontract'],
                              })

        if(cnt % 100000 == 0):
            if(len(contract_bars) > 0):
                collection.insert_many(contract_bars)

            contract_bars = []

        cnt += 1
    except TypeError:
        print('TypeError')
        print(row)
        break

    #if cnt > 3:
    #    break

    pbar.update(1)

#print(contract_settlements)

if(len(contract_bars) > 0):
    result  = collection.insert_many(contract_bars)

#print(result.inserted_ids)


'''