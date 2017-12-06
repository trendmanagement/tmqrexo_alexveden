from pymongo import MongoClient
from tradingcore.execution_manager import ExecutionManager
from tradingcore.campaign import Campaign
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.exostorage import EXOStorage
from scripts.settings import *
from smartcampaign import SmartCampaignBase
import traceback

from tradingcore.messages import *
from tradingcore.signalapp import SignalApp, APPCLASS_UTILS

signalapp = SignalApp("SmartCampaignDaily", APPCLASS_UTILS, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)
signalapp.send(MsgStatus('INIT', 'Updating Smart Campaign Weights', notify=True))

storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, futures_limit=10, options_limit=10, exostorage=storage)
exmgr = ExecutionManager(MONGO_CONNSTR, datasource, dbname=MONGO_EXO_DB)


client = MongoClient(MONGO_CONNSTR)
db = client[MONGO_EXO_DB]
accounts_collection = db['accounts']
accounts_equity_collection = db['accounts_equity']

# Update accounts linked with SmartCampaigns
for acct_dict in accounts_collection.find({'mmclass_name': 'smart'}):
    signalapp.send(MsgStatus('RUN', 'Processing: {0}'.format(acct_dict), notify=False))

    account_equity_val = 100000

    try:
        account_equity = list(accounts_equity_collection.find({'name':acct_dict['name']}, {'equity_list':{'$slice':-1}}))

        if account_equity:
            account_equity_val = account_equity[0]['equity_list'][0]['equity']
        else:
            signalapp.send(MsgStatus('ERR', "There is not an equity entry for : \n\n" + acct_dict['name'], notify=True))

    except Exception as exc:
        signalapp.send(MsgStatus('ERR', "Exception: \n\n" + traceback.format_exc(), notify=True))


    try:

        accounts_collection.update({'_id': acct_dict['_id']},
                                   {'$set': {
                                       # TODO: !!! Change this placeholder value by real account equity value!
                                       "info.smart_equity": account_equity_val,
                                   }
                                   });

    except Exception as exc:
        signalapp.send(MsgStatus('ERR', "Exception: \n\n" + traceback.format_exc(), notify=True))


signalapp.send(MsgStatus('RUN', 'Smart campaign updates finished', notify=True))
