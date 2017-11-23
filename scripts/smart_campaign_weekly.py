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

signalapp = SignalApp("SmartCampaignWeekly", APPCLASS_UTILS, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)
signalapp.send(MsgStatus('INIT', 'Updating Smart Campaign Weights', notify=True))

storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, futures_limit=10, options_limit=10, exostorage=storage)
exmgr = ExecutionManager(MONGO_CONNSTR, datasource, dbname=MONGO_EXO_DB)


client = MongoClient(MONGO_CONNSTR)
db = client[MONGO_EXO_DB]
scmp_collection = db['campaigns_smart']


for scmp_dict in scmp_collection.find({}, projection={'name': True}):
    scmp_name = scmp_dict['name']
    signalapp.send(MsgStatus('RUN', 'Processing: {0}'.format(scmp_name), notify=True))
    try:
        scmp = SmartCampaignBase.load_from_v1(scmp_name, storage, scmp_collection)
        # Recalculate SmartCampaign weights and export
        v1_cmp_dict = scmp.export_to_v1_campaign()

        # Save to v1 campaign
        cmp = Campaign(v1_cmp_dict, datasource)
        exmgr.campaign_save(cmp)
    except Exception as exc:
        signalapp.send(MsgStatus('ERR', "Exception: \n\n" + traceback.format_exc(), notify=True))


signalapp.send(MsgStatus('RUN', 'Smart campaign updates finished', notify=True))
