import unittest
from tradingcore.campaign_bridge import CampaignBridge
from exobuilder.data.exostorage import EXOStorage
from scripts.settings import *
from tradingcore.campaign import Campaign


class CampaignBridgeTestCase(unittest.TestCase):
    def test_swarms_list(self):
        cbr = CampaignBridge()

        cbr.swarms_list()

    def test_swarms_get_campaign_alphas_net_position(self):
        alphas = {'!NEW_ES_debug_alpha_online_recalc': {'qty': 10.0},
                  '!NEW_ES_debug_alpha_online_recalc2': {'qty': 10.0}}
        cbr = CampaignBridge()

        alphas_position = cbr.get_alphas_raw_positions(alphas)

        merged_pos = cbr.merge_alphas_positions(alphas_position)

        pass

    def test_get_alpha_transactions_list(self):
        alphas = {'!NEW_ES_debug_alpha_online_recalc': {'qty': 10.0},
                  '!NEW_ES_debug_alpha_online_recalc2': {'qty': 10.0}}
        cbr = CampaignBridge()
        transactions = cbr.get_alphas_transactions_list(alphas)

        pass


    def test_swarms_list_storage(self):
        storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

        instruments_filter = ['ES']  # Select ALL
        # instruments_filter = ['ES', 'CL']

        exo_filter = ['ES']  # Select ALL
        # exo_filter = ['BullishCollar']

        direction_filter = [0, -1, 1]  # Select ALL
        # direction_filter = [1]

        alpha_filter = ['*']  # Select ALL
        # alpha_filter = ['April_24','April_25']

        swmdf, swm_data = storage.swarms_list(instruments_filter, direction_filter, alpha_filter, exo_filter)

    def test_campaign_position(self):
        alphas = {
            'ES_CallSpread_Long_MACross__Bullish_1_April_25_custom': {'qty': 1.0},
            '!NEW_ES_debug_alpha_online_recalc': {'qty': 10.0},
            '!NEW_ES_debug_alpha_online_recalc2': {'qty': 10.0},
        }

        from tradingcore.execution_manager import ExecutionManager
        from tradingcore.campaign import Campaign
        from exobuilder.data.datasource_mongo import DataSourceMongo
        from exobuilder.data.assetindex_mongo import AssetIndexMongo

        storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, futures_limit=10, options_limit=10,
                                     exostorage=storage)
        #exmgr = ExecutionManager(MONGO_CONNSTR, datasource, dbname=MONGO_EXO_DB)

        CAMPAIGN_NAME = 'TEST_TEST_TEST'
        CAMPAIGN_DESCRIPTION = ""
        campaign_dict = {
            'name': CAMPAIGN_NAME,
            'description': CAMPAIGN_DESCRIPTION,
            'alphas': alphas
        }

        cmp = Campaign(campaign_dict, datasource)

        pos = cmp.positions

        pass

    def test_campaign_position_at_date(self):
        alphas = {
            'ES_CallSpread_Long_MACross__Bullish_1_April_25_custom': {'qty': 1.0},
            '!NEW_ES_debug_alpha_online_recalc': {'qty': 10.0},
            '!NEW_ES_debug_alpha_online_recalc2': {'qty': 10.0},
        }

        from tradingcore.execution_manager import ExecutionManager
        from tradingcore.campaign import Campaign
        from exobuilder.data.datasource_mongo import DataSourceMongo
        from exobuilder.data.assetindex_mongo import AssetIndexMongo

        storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, futures_limit=10, options_limit=10,
                                     exostorage=storage)
        #exmgr = ExecutionManager(MONGO_CONNSTR, datasource, dbname=MONGO_EXO_DB)

        CAMPAIGN_NAME = 'TEST_TEST_TEST'
        CAMPAIGN_DESCRIPTION = ""
        campaign_dict = {
            'name': CAMPAIGN_NAME,
            'description': CAMPAIGN_DESCRIPTION,
            'alphas': alphas
        }

        cmp = Campaign(campaign_dict, datasource)

        pos = cmp.positions_at_date()

        pass



if __name__ == '__main__':
    unittest.main()
