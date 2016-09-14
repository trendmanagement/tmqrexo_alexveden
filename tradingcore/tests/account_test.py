import unittest
from tradingcore.account import Account
from bson.objectid import ObjectId
from pymongo import MongoClient

class AccountTestCase(unittest.TestCase):
    def setUp(self):
        self._dict = {
            'name': 'test_account',
            'client_name': 'test_client',
            '_id': ObjectId("57b42aba82d9c39e0341fbc7")
        }

        client = MongoClient('mongodb://localhost:27017/')
        self._db = client['tmqr_testdb']

        self._acc = Account(self._dict, self._db)

    def test_init(self):
        acc = Account(self._dict, self._db)

        self.assertEqual(self._dict, acc._dict)
        self.assertEqual(self._db, acc._db)

    def test_has_name(self):
        self.assertEqual('test_account', self._acc.name)

    def test_has_client_name(self):
        self.assertEqual('test_client', self._acc.client_name)

    def test_has_dbid(self):
        self.assertEqual(ObjectId("57b42aba82d9c39e0341fbc7"), self._acc.dbid)



if __name__ == '__main__':
    unittest.main()
