from pymongo.mongo_client import MongoClient
from tradingcore.campaign import Campaign
from tradingcore.account import Account
from tradingcore.moneymanagement import MM_CLASSES


class ExecutionManager:
    def __init__(self, conn_str, datasource, dbname='tmldb'):
        self.client = MongoClient(conn_str)
        self.db = self.client[dbname]
        self.datasource = datasource
        self._campaign_cache = {}

    def campaign_save(self, campaign):
        campaign_collection = self.db['campaigns']
        campaign_collection.replace_one({'name': campaign.name}, campaign.as_dict(), upsert=True)

    def campaign_load(self, campaign_name):
        campaign_collection = self.db['campaigns']

        campaign_dict = campaign_collection.find_one({'name': campaign_name})
        return Campaign(campaign_dict, self.datasource)

    def campaign_load_all(self):
        campaign_collection = self.db['campaigns']

        campaigns = {}
        for cmp_dict in campaign_collection.find():
            cmp_instance = Campaign(cmp_dict, self.datasource)
            campaigns[cmp_instance.name] = cmp_instance

        self._campaign_cache = campaigns
        return campaigns

    def account_save(self, account):
        account_collection = self.db['accounts']
        account_collection.replace_one({'name': account.name}, account.as_dict(), upsert=True)

    def account_load(self, account_name):
        account_collection = self.db['accounts']
        acc_dict = account_collection.find_one({'name': account_name})

        if acc_dict['campaign_name'] in self._campaign_cache:
            acc_campaign = self._campaign_cache[acc_dict['campaign_name']]
        else:
            acc_campaign = self.campaign_load(acc_dict['campaign_name'])

        mmclass = MM_CLASSES[acc_dict['mmclass_name']]

        return Account(acc_dict, acc_campaign, mmclass(acc_dict['info']))
