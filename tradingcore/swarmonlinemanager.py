from exobuilder.data.exostorage import EXOStorage
from backtester.swarms.swarm import Swarm
import pymongo
from pymongo import MongoClient
from datetime import datetime
from backtester.strategy import OptParamArray


class SwarmOnlineManager:
    def __init__(self, mongo_connstr, mongo_dbname, strategy_context):
        self.client = MongoClient(mongo_connstr)
        self.db = self.client[mongo_dbname]
        self.strategy_context = strategy_context

        self.mongo_connstr = mongo_connstr
        self.mongo_dbname = mongo_dbname

    def save(self, swm, global_context={}):
        """
        Stores information about swarm state in the MongoDB
        :param direction: Long/short [1 ; -1]
        :param smgr: SwarmManager class instance
        :param global_context:  dict for additional info
        :return:
        """
        data = swm.laststate_to_dict()
        data['global_context'] = global_context

        # Storing data in the DB
        self.db['swarms'].replace_one({'swarm_name': swm.name}, data, upsert=True)

    def load(self, exo_name, alpha_name):
        result = []
        for sctx in self.db['swarms'].find({'alpha_name': alpha_name, 'exo_name': exo_name}):
            result.append(sctx)
        return result


    def process(self, exo_name, swm_callback=None):
        """
        Run this method every time when new EXO quote comes
        :param exo_name: exo_name in MongoDB
        :param swm_callback: swarm_callback after swarm is updated
        :return:
        """
        # Read EXO quote data from Mongo
        exo_storage = EXOStorage(self.mongo_connstr, self.mongo_dbname)

        # Read swarm parameters from Mongo
        StrategyClass = self.strategy_context['strategy']['class']

        # Load All swarms for Strategy and EXO name
        swarms_data = self.load(exo_name, StrategyClass.name)

        if len(swarms_data) > 0:
            # Check EXO data length
            exo_df, exo_info = exo_storage.load_series(exo_name)
            if len(exo_df) == 0 or len(exo_df) < 200 or (datetime.now() - exo_df.index[-1]).days > 4:
                last_exo_date = 'N/A' if len(exo_df) == 0 else exo_df.index[-1]
                raise ValueError('Not actual or empty EXO data found in {0} last date {1}'.format(exo_name,
                                                                                                  last_exo_date))

        for swm_dict in swarms_data:
            # Generate context for swarm
            context = self.strategy_context
            context['strategy']['exo_storage'] = exo_storage
            context['strategy']['exo_name'] = exo_name
            direction = swm_dict['direction']
            if direction == 0:
                dir_array = [-1, 1]
            else:
                dir_array = [direction]
            context['strategy']['opt_params'][0] = OptParamArray('Direction', dir_array)

            # Restoring swarms last state from dict
            swm = Swarm.laststate_from_dict(swm_dict, context)


            # Update swarm equity dynamic and last state
            swm.update()

            # Saving swarm state to Mongo
            self.save(swm)

            if swm_callback is not None:
                # Run Swarm callback (to notify framework that swarm is updated)
                swm_callback(swm)


