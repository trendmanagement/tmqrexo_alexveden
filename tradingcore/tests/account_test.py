import unittest
from tradingcore.account import Account
from bson.objectid import ObjectId
from pymongo import MongoClient
from tradingcore.moneymanagement import PlainMM
from tradingcore.campaign import Campaign
from tradingcore.tests.campaign_test import DataSourceTest1

class AccountTestCase(unittest.TestCase):
    def setUp(self):
        self._dict = {
            'name': 'test_account',
            'client_name': 'test_client',
            '_id': ObjectId("57b42aba82d9c39e0341fbc7"),
            'info': {
                'size_factor': 1.0,
            }

        }

        self._camp_dict = {
            'name': 'test_campaign',
            'description': 'Brief description of campaign',
            '_id': ObjectId("57b42aba82d9c39e0341fbc7"),
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

        self._datasource = DataSourceTest1()
        self._cmp = Campaign(self._camp_dict, self._datasource)

        self.mmclass = PlainMM(self._dict['info'])

        self._acc = Account(self._dict, self._cmp, self.mmclass)

    def test_init(self):
        acc = Account(self._dict, self._cmp, self.mmclass)
        self.assertEqual(self._cmp, acc.campaign)
        self.assertEqual(self.mmclass, acc.mmclass)

    def test_has_name(self):
        self.assertEqual('test_account', self._acc.name)

    def test_has_client_name(self):
        self.assertEqual('test_client', self._acc.client_name)



if __name__ == '__main__':
    unittest.main()

