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

# Update accounts linked with SmartCampaigns
for acct_dict in accounts_collection.find({'mmclass_name': 'smart'}):
    signalapp.send(MsgStatus('RUN', 'Processing: {0}'.format(acct_dict), notify=False))
    try:
        accounts_collection.update({'_id': acct_dict['_id']},
                                   {'$set': {
                                       # TODO: !!! Change this placeholder value by real account equity value!
                                       "info.smart_equity": 10000,
                                   }
                                   });

    except Exception as exc:
        signalapp.send(MsgStatus('ERR', "Exception: \n\n" + traceback.format_exc(), notify=True))


signalapp.send(MsgStatus('RUN', 'Smart campaign updates finished', notify=True))
