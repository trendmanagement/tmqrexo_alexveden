from pymongo import MongoClient
from tradingcore.execution_manager import ExecutionManager
from tradingcore.campaign import Campaign
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.exostorage import EXOStorage
from scripts.settings import *
from smartcampaign import SmartCampaignBase
import traceback

from backtester.reports.campaign_real_compare_report import CampaignRealCompare
from datetime import datetime, date, timedelta, time as dttime

from tradingcore.messages import *
from tradingcore.signalapp import SignalApp, APPCLASS_UTILS

try:
    signalapp = SignalApp("SmartCampaignDaily", APPCLASS_UTILS, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)
    signalapp.send(MsgStatus('INIT', 'Updating Smart Campaign Weights', notify=True))
except Exception as exc:
    print(exc)

storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, futures_limit=10, options_limit=10, exostorage=storage)
exmgr = ExecutionManager(MONGO_CONNSTR, datasource, dbname=MONGO_EXO_DB)


client = MongoClient(MONGO_CONNSTR)
db = client[MONGO_EXO_DB]
accounts_collection = db['accounts']
accounts_equity_collection = db['accounts_equity']

# Update accounts linked with SmartCampaigns
for acct_dict in accounts_collection.find({'mmclass_name': 'smart','campaign_name':'ES_SmartCampaign_V5_RelStr_Concept'}):

    try:
        signalapp.send(MsgStatus('RUN', 'Processing: {0}'.format(acct_dict), notify=False))
    except Exception as exc:
        print(exc)

    # *******************************************************************
    '''
    This is just for the test accounts with 'client_name': 'TEST'
    Below takes the latest account equity from accounts_equity and pushes up a new value adjust with the model change  
    '''
    try:
        num_of_days_back_master = 1

        client = MongoClient(MONGO_CONNSTR)
        # db = client[MONGO_EXO_DB]
        # accounts_collection = db['accounts']
        # accounts_equity_collection = db['accounts_equity']

        crc = CampaignRealCompare()

        # for acct_dict in accounts_collection.find({'mmclass_name': 'smart', 'client_name': 'TEST'}):
        if acct_dict['client_name'] == 'TEST':

            archive_based_pnl_dict = crc.get_account_positions_archive_pnl_multiproduct(
                # costs_per_contract=3.0 # Default
                # costs_per_option=3.0 # Default                                                          .
                num_days_back=1,
                fcm_office=acct_dict['FCM_OFFICE'], fcm_acct=acct_dict['FCM_ACCT'],
                return_transactions=True,
            )

            total_pl_change = 0.0
            try:
                for instrument, pnl_values in archive_based_pnl_dict.items():
                    total_pl_change = pnl_values['pnls']['SettleChange'].iloc[-1]
            except Exception as exc:
                print(exc)


            account_equity = list(
                accounts_equity_collection.find({'name': acct_dict['name']}, {'equity_list': {'$slice': -2}}))
            if account_equity:

                equity_list = account_equity[0]['equity_list']

                last_account_equity = account_equity[0]['equity_list'][-1]['equity']

                if account_equity[0]['equity_list'][-1]['date'].date() != datetime.now().date():
                    last_account_equity += total_pl_change
                elif len(equity_list) > 1:
                    last_account_equity = account_equity[0]['equity_list'][-2]['equity'] + total_pl_change

                dt = datetime.combine(datetime.now().date(), dttime(0, 0, 0))

                updateResult = accounts_equity_collection.update_one({'name': acct_dict['name']},
                                                                     {
                                                                         '$pull': {
                                                                             'equity_list': {'date': dt},
                                                                         }
                                                                     }, upsert=True)

                updateResult = accounts_equity_collection.update_one({'name': acct_dict['name']},
                                                                     {
                                                                         '$addToSet': {
                                                                             'equity_list': {'date': dt,
                                                                                             'equity': last_account_equity},
                                                                         }
                                                                     }, upsert=True)

                # print('Updating accounts_equity collection account name {0} {1} smart equity {2}'
                #       .format(acct_dict['name'], dt, last_account_equity))

    except Exception as exc:
        try:
            signalapp.send(MsgStatus('ERR', "Exception: \n\n" + traceback.format_exc(), notify=True))
        except Exception as exc:
            print(exc)
    # *******************************************************************

    account_equity_val = 100000

    try:
        account_equity = list(accounts_equity_collection.find({'name':acct_dict['name']}, {'equity_list':{'$slice':-1}}))

        if account_equity:
            account_equity_val = account_equity[0]['equity_list'][0]['equity']
        else:
            try:
                signalapp.send(MsgStatus('ERR', "There is not an equity entry for : \n\n" + acct_dict['name'], notify=True))
            except Exception as exc:
                print(exc)

    except Exception as exc:
        try:
            signalapp.send(MsgStatus('ERR', "Exception: \n\n" + traceback.format_exc(), notify=True))
        except Exception as exc:
            print(exc)


    try:

        accounts_collection.update({'_id': acct_dict['_id']},
                                   {'$set': {
                                       # TODO: !!! Change this placeholder value by real account equity value!
                                       "info.smart_equity": account_equity_val,
                                   }
                                   });

    except Exception as exc:
        try:
            signalapp.send(MsgStatus('ERR', "Exception: \n\n" + traceback.format_exc(), notify=True))
        except Exception as exc:
            print(exc)






try:
    signalapp.send(MsgStatus('RUN', 'Smart campaign updates finished', notify=True))
except Exception as exc:
    print(exc)
