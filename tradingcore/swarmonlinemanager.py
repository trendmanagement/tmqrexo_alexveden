from exobuilder.data.exostorage import EXOStorage

import pymongo
from pymongo import MongoClient
from datetime import datetime
import pickle

class SwarmOnlineManager:
    def __init__(self, mongo_connstr, mongo_dbname, strategy_context):
        self.client = MongoClient(mongo_connstr)
        self.db = self.client[mongo_dbname]
        self.strategy_context = strategy_context

        self.mongo_connstr = mongo_connstr
        self.mongo_dbname = mongo_dbname

    def save(self, direction, smgr, global_context={}):
        """
        Stores information about swarm state in the MongoDB
        :param direction: Long/short [1 ; -1]
        :param smgr: SwarmManager class instance
        :param global_context:  dict for additional info
        :return:
        """
        # TODO: AttributeError: 'int' object has no attribute 'swarm_ispicked'
        df_picked = smgr.swarm_ispicked.tail(1).T
        picked_aplhas = df_picked[df_picked[df_picked.columns[0]] == 1]
        alpha_params = []
        for a in picked_aplhas.index:
            alpha_params.append({
                'opt_params': a
            })

        context = global_context.copy()
        context['global_filter'] = True # Dummy # TODO: add support of global filter

        data = {
            'swarm_name': smgr.get_swarm_name(),
            'exo_name': smgr.get_exo_name(),
            'alpha_name': smgr.strategy.name,
            'direction': direction,
            'alpha_params': alpha_params,
            'global_context': context,
            'update_date': datetime.now(),
            'rebalance_date': datetime.now(),
            'equity': pickle.dumps(smgr.swarm_picked.sum(axis=1))
        }

        # Storing data in the DB
        self.db['swarms'].replace_one({'swarm_name': smgr.get_swarm_name()}, data, upsert=True)

    def load(self, exo_name, alpha_name):
        result = []
        for sctx in self.db['swarms'].find({'alpha_name': alpha_name, 'exo_name': exo_name}):
            result.append(sctx)
        return result

    def process(self, exo_name):
        """
        Run this method every time when new EXO quote comes
        :param exo_name:
        :return:
        """
        # Read EXO quote data from Mongo
        exo_storage = EXOStorage(self.mongo_connstr, self.mongo_dbname)

        # Read swarm parameters from Mongo
        StrategyClass = self.strategy_context['strategy']['class']

        # Load All swarms for Strategy and EXO name
        swarms_context = self.load(exo_name, StrategyClass.name)

        for swmctx in swarms_context:
            pass
            # Create strategies instances for each opt_params set

            # Calculate strategies (get inposition value)

            # Calculate swarm of strategies

            # Calculate sum swarm equity

            # Write recent state to Mongo
                # Update swarm equity data
                # Update each swarm position

            # Notify trading engine that swarm was calculated (?)


