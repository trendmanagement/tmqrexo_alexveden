from pymongo.mongo_client import MongoClient
from tradingcore.campaign import Campaign
from tradingcore.account import Account
from tradingcore.moneymanagement import MM_CLASSES
from datetime import datetime


class ExecutionManager:
    def __init__(self, conn_str, datasource, dbname='tmldb'):
        self.client = MongoClient(conn_str)
        self.db = self.client[dbname]
        self.datasource = datasource
        self._campaign_cache = {}

    def campaign_save(self, campaign, force=False):
        """
        Saves campaign instance to MongoDB
        :param campaign: Campaign class instance
        :param force: Skip sanity checks and force campaign write to DB
        :return: None
        """
        campaign_collection = self.db['campaigns']

        existing_campaign = campaign_collection.find_one({'name': campaign.name})

        sanity_passed = True

        if existing_campaign and not force:
            # Do sanity checks
            for exesting_alpha, existing_val in existing_campaign['alphas'].items():
                if 'begin' in existing_val:
                    if 'begin' not in campaign.alphas[exesting_alpha] or existing_val['begin'] != \
                            campaign.alphas[exesting_alpha]['begin']:
                        sanity_passed = False
                        print(
                            "WARNING: {0} have 'begin' setting in the DB, but it's not set in new records or not equal".format(
                                exesting_alpha))

                if 'end' in existing_val:
                    if 'end' not in campaign.alphas[exesting_alpha] or existing_val['end'] != \
                            campaign.alphas[exesting_alpha]['end']:
                        print(
                            "WARNING: {0} have 'end' setting in the DB, but it's not set in new records or not equal".format(
                                exesting_alpha))
                        sanity_passed = False


        if sanity_passed:
            campaign_collection.replace_one({'name': campaign.name}, campaign.as_dict(), upsert=True)
            print("Done")
        else:
            print("(!) Sanity checks are failed, check the campaign settings and run campaign_save() with force=True")

    def campaign_load(self, campaign_name):
        """
        Loads campaign instance by name
        :param campaign_name:
        :return:
        """
        campaign_collection = self.db['campaigns']
        campaign_dict = campaign_collection.find_one({'name': campaign_name})
        return Campaign(campaign_dict, self.datasource)

    def campaign_load_all(self):
        """
        Load and cache all campaign instances
        :return:
        """
        campaign_collection = self.db['campaigns']

        campaigns = {}
        for cmp_dict in campaign_collection.find():
            cmp_instance = Campaign(cmp_dict, self.datasource)
            campaigns[cmp_instance.name] = cmp_instance

        # Cache all campaigns (used for fast accounts population)
        self._campaign_cache = campaigns
        return campaigns

    def account_save(self, account):
        """
        Saves Account class instance to Mongo
        :param account: account instance
        :return:
        """
        account_collection = self.db['accounts']
        account_collection.replace_one({'name': account.name}, account.as_dict(), upsert=True)

    def account_load(self, account_name):
        """
        Load Account instance by name
        :param account_name: account name in Mongo collection
        :return:
        """
        account_collection = self.db['accounts']
        acc_dict = account_collection.find_one({'name': account_name})
        return self.account_process(acc_dict)

    def account_load_all(self):
        """
        Load Account instance by name
        :param account_name: account name in Mongo collection
        :return:
        """
        result = {}
        account_collection = self.db['accounts']
        for acc_dict in account_collection.find({}):
            acc = self.account_process(acc_dict)
            result[acc.name] = acc
        return result

    def account_process(self, acc_dict):
        """
        Process Account instance from Mongo account dict
        :param acc_dict:
        :return:
        """
        if acc_dict['campaign_name'] in self._campaign_cache:
            # Return cached result if exists
            acc_campaign = self._campaign_cache[acc_dict['campaign_name']]
        else:
            # Load campaign directly from MongoDB
            acc_campaign = self.campaign_load(acc_dict['campaign_name'])

        # Get MoneyManagement class from pre-defined list (by name)
        mmclass = MM_CLASSES[acc_dict['mmclass_name']]

        isactive = True
        if 'isactive' in acc_dict:
            isactive = acc_dict['isactive']

        # Return new Account class instance
        return Account(acc_dict, acc_campaign, mmclass(acc_dict['info']), isactive)

    def account_positions_process(self, write_to_db=False):
        """
        Process all accounts positions from Mongo and save them into collection
        :param write_to_db: if True - save all account positions to MongoDB
        :return:
        """
        account_collection = self.db['accounts']
        acc_list = account_collection.find()

        # Populate campaign list cache
        self.campaign_load_all()

        # Prepare bulk MongoDB request
        bulk = self.db['accounts_positions'].initialize_ordered_bulk_op()
        bulk.find({}).remove()

        # Populating account positions
        account_positions = {}

        for acc_dict in acc_list:
            # Create new account instance
            acc = self.account_process(acc_dict)
            if not acc.isactive:
                continue
            # Get account positions processed by MM algorithm
            acc_pos = acc.positions

            # Add position dict to MongoDB bulk write operation
            result_dict = acc_dict
            result_dict['positions'] = acc_pos
            result_dict['date_now'] = datetime.now()
            bulk.insert(result_dict)
            account_positions[acc.name] = result_dict

        if write_to_db:
            # Execute bulk insert into MongoDB
            bulk.execute()
        return account_positions
