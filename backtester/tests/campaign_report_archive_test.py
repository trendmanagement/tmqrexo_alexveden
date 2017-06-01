import unittest
from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.tests.assetindexdict import AssetIndexDicts
from datetime import datetime, date, timedelta, time as dttime
from exobuilder.contracts.instrument import Instrument
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.datasource_sql import DataSourceSQL
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.exostorage import EXOStorage
from exobuilder.exo.exoenginebase import ExoEngineBase
from exobuilder.exo.transaction import Transaction
import time
from exobuilder.algorithms.rollover_helper import RolloverHelper
from copy import deepcopy
import importlib

from datetime import datetime
from collections import OrderedDict
from exobuilder.exo.position import Position
from scripts.settings import *
from pymongo import MongoClient
from tradingcore.campaign import Campaign


import pprint

from backtester.reports.campaign_report import CampaignReport
from backtester.reports.campaign_real_compare_report import CampaignRealCompare

class CampaignReportArchiveTestCase(unittest.TestCase):

    def test_position_pnl_settlement(self):
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

        futures_limit = 3
        options_limit = 10

        num_of_days_back_master = 10
        datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, futures_limit, options_limit, storage)

        campaign_dict = storage.campaign_load('ES_Bidirectional V3')
        cmp = Campaign(campaign_dict, datasource)

        dt = datetime(2017, 5, 16)

        cmp_pos = cmp.positions_at_date(dt)


        asset_info = assetindex.get_instrument_info('ES')
        exec_time_end, decision_time_end = AssetIndexMongo.get_exec_time(dt, asset_info)


        position = Position()

        for contract, pos_dict in cmp_pos.netpositions.items():
            if pos_dict['qty'] == 0:
                continue

            contract = datasource.get(contract.__hash__(), decision_time_end)
            position.add(Transaction(contract, decision_time_end, pos_dict['qty']))

        all_pos_contracts = set(cmp_pos.netpositions.keys()) & set(position.netpositions)
        self.assertEqual(len(all_pos_contracts), len(cmp_pos.netpositions))
        self.assertEqual(len(all_pos_contracts), len(position.netpositions))

        # Comparing QTY
        for cname in all_pos_contracts:
            self.assertEqual(cmp_pos.netpositions[cname]['qty'], position.netpositions[cname]['qty'])

        cmp_pos_curr = cmp.positions_at_date(dt, datetime(2017, 5, 17))
        cmp_pnl = cmp_pos_curr.pnl_settlement - cmp_pos.pnl_settlement

        old_pnl = position.pnl_settlement
        position.set_date(datasource, datetime(2017, 5, 17))
        pos_pnl = position.pnl_settlement - old_pnl

        self.assertEqual(cmp_pnl, pos_pnl)



    def test_report_positions_compare(self):
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

        futures_limit = 3
        options_limit = 10

        num_of_days_back_master = 10

        # datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, assetindex, futures_limit, options_limit, storage)
        datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, futures_limit, options_limit, storage)

        #rpt = CampaignReport('ES_Bidirectional V3', datasource, pnl_settlement_ndays=num_of_days_back_master + 1)

        crc = CampaignRealCompare()
        #archive_based_pnl = crc.get_account_positions_archive_pnl(account_name="CLX60125",
        #                                                          instrument="ES",
        #                                                          # costs_per_contract=3.0 # Default
        #                                                          # costs_per_option=3.0 # Default
        #                                                          )

        campaign_dict = storage.campaign_load('ES_Bidirectional V3')
        cmp = Campaign(campaign_dict, datasource)

        account_name = "CLX60125"
        instrument = "ES"
        num_days_back = 10
        position_dict = OrderedDict()
        costs_per_contract = 3.0
        costs_per_option = 3.0
        mongoClient = MongoClient(MONGO_CONNSTR)
        db = mongoClient[MONGO_EXO_DB]

        for pos in reversed(list(
                db['accounts_positions_archive'].find({'name': account_name}).sort([('date_now', -1)]).limit(
                        num_days_back))):
            # print(pos)

            dt = pos['date_now']
            pos_rec = position_dict.setdefault(dt, {})

            for p in pos['positions']:
                if '_hash' not in p['asset']:
                    break

                pos_rec[p['asset']['_hash']] = p['qty']

        prev_position = None

        account_pnl = []
        costs = []
        account_pnl_index = []

        p_dict = Position().as_dict()

        tmp_position_arch_prev = None
        tmp_position_cmp_prev = None
        tmp_prev_date = None

        for d, pos_rec in position_dict.items():
            costs_sum = 0.0





            if tmp_position_cmp_prev is not None:
                position = Position.from_dict(p_dict, datasource, decision_time_end)

                new_exec_time_end, new_decision_time_end = AssetIndexMongo.get_exec_time(d, asset_info)

                cmp_curr = cmp.positions_at_date(tmp_prev_date, new_decision_time_end)
                cmp_prev = cmp.positions_at_date(tmp_prev_date)

                #
                # Do sanity checks to compare previous postions
                #
                all_pos_contracts = set(cmp_curr.netpositions.keys()) & set(tmp_position_arch_prev.netpositions)
                self.assertEqual(len(all_pos_contracts), len(cmp_curr.netpositions))
                self.assertEqual(len(all_pos_contracts), len(tmp_position_arch_prev.netpositions))

                for cname in all_pos_contracts:
                    self.assertEqual(tmp_position_arch_prev.netpositions[cname]['qty'],
                                     cmp_curr.netpositions[cname]['qty'])

                cmp_pnl1 = cmp_curr.pnl_settlement - cmp_prev.pnl_settlement
                #cmp_pnl2 = campaign_position.pnl_settlement - tmp_position_cmp_prev.pnl_settlement
                #arch_pnl = position.pnl_settlement - tmp_position_arch_prev.pnl_settlement

                tmp_prev_pnl = position.pnl_settlement
                position.set_date(datasource, new_decision_time_end)
                arch_pnl2 = position.pnl_settlement - tmp_prev_pnl

                self.assertAlmostEqual(cmp_pnl1, arch_pnl2, 1)
                pass

            asset_info = assetindex.get_instrument_info(instrument)
            exec_time_end, decision_time_end = AssetIndexMongo.get_exec_time(d, asset_info)

            position = Position.from_dict(p_dict, datasource, decision_time_end)

            transactions = CampaignRealCompare._calc_transactions(d, pos_rec, prev_position)

            for contract_hash, qty in transactions.items():
                if qty == 0:
                    continue

                contract = datasource.get(contract_hash, decision_time_end)
                position.add(Transaction(contract, decision_time_end, qty))

                if isinstance(contract, FutureContract):
                    costs_sum += -abs(costs_per_contract) * abs(qty)
                else:
                    costs_sum += -abs(costs_per_option) * abs(qty)

            try:
                pnl = position.pnl_settlement + costs_sum
            except:
                pnl = float('nan')

            prev_position = pos_rec
            p_dict = position.as_dict()

            #
            # Check that actual position qty and campaign position match
            #
            campaign_position = cmp.positions_at_date(d)

            cmp_net_pos = campaign_position.netpositions
            arch_net_pos = position.netpositions

            all_pos_contracts = set(cmp_net_pos.keys()) & set(arch_net_pos)
            self.assertEqual(len(all_pos_contracts), len(cmp_net_pos))
            self.assertEqual(len(all_pos_contracts), len(arch_net_pos))

            # Comparing QTY
            for cname in all_pos_contracts:
                self.assertEqual(cmp_net_pos[cname]['qty'], arch_net_pos[cname]['qty'])




            tmp_position_arch_prev = position
            tmp_position_cmp_prev = campaign_position
            tmp_prev_date = d






if __name__ == '__main__':
    unittest.main()
