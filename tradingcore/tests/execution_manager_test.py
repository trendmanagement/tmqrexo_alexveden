import unittest
from tradingcore.execution_manager import ExecutionManager
from tradingcore.campaign import Campaign
from tradingcore.account import Account
from tradingcore.moneymanagement import PlainMM
from tradingcore.tests.campaign_test import DataSourceTest1

class ExecutionManagerTestCase(unittest.TestCase):

    def setUp(self):
        mongo_connstr = 'mongodb://localhost:27017/'
        mongo_db_name = 'tmldb_test'
        self.exmgr = ExecutionManager(mongo_connstr, datasource=DataSourceTest1(), dbname=mongo_db_name)

    def test_campaign_save(self):
       _dict = {
            'name': 'test_campaign',
            'description': 'Brief description of campaign',
            'alphas': {
                'alpha1': {
                    'qty': -1.0,
                    'leg_name': 'leg1',
                },
                'alpha2': {
                    'qty': -2.0,
                },
                'alpha3': {
                    'qty': 2.0,
                    'leg_name': 'leg2',
                },
            }
       }
       _cmp = Campaign(_dict, None)
       self.exmgr.campaign_save(_cmp)

    def test_campaign_load(self):
        cmp = self.exmgr.campaign_load('test_campaign')
        self.assertEqual(Campaign, type(cmp))
        self.assertEqual('test_campaign', cmp.name)

    def test_campaign_load_all(self):
        cmp_dict = self.exmgr.campaign_load_all()
        self.assertEqual(dict, type(cmp_dict))

    def test_account_save(self):
        _dict = {
            'name': 'test_account',
            'client_name': 'test_client',
            'info': {
                'size_factor': 1.0
            }
        }

        acc = Account(_dict, self.exmgr.campaign_load('test_campaign'), PlainMM(_dict['info']))
        self.exmgr.account_save(acc)

    def test_account_load(self):
        acc = self.exmgr.account_load('test_account')
        self.assertEqual(type(acc), Account)
        self.assertEqual(acc.name, 'test_account')
        self.assertEqual(acc.campaign.name, 'test_campaign')
        self.assertEqual(acc.mmclass.name(), 'plain')

    def test_account_load_from_cache(self):
        # exmgr.campaign_load_all fills the cache
        cmp_dict = self.exmgr.campaign_load_all()

        acc = self.exmgr.account_load('test_account')
        self.assertEqual(type(acc), Account)
        self.assertEqual(acc.name, 'test_account')
        self.assertEqual(acc.campaign.name, 'test_campaign')
        self.assertEqual(acc.mmclass.name(), 'plain')

    def test_account_positions_process(self):
        # exmgr.campaign_load_all fills the cache
        cmp_dict = self.exmgr.account_positions_process()





if __name__ == '__main__':
    unittest.main()

