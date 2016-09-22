try:
    from .settings import *
except SystemError:
    from scripts.settings import *

try:
    from .settings_local import *
except SystemError:
    try:
        from scripts.settings_local import *
    except ImportError:
        pass
    pass


import os, sys
import importlib
from backtester.swarms.swarm import Swarm
from backtester.strategy import OptParamArray
from exobuilder.data.exostorage import EXOStorage
from tradingcore.swarmonlinemanager import SwarmOnlineManager
import logging


TMQRPATH = os.getenv("TMQRPATH", '')

logger = logging.getLogger('AlphaRebalancerScript')
loglevel = logging.DEBUG
logger.setLevel(loglevel)

# create file handler which logs even debug messages
fh = logging.FileHandler(os.path.join(TMQRPATH, 'alpha_rebalancer.log'))
fh.setLevel(loglevel)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(loglevel)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
fh.setFormatter(formatter)
logger.addHandler(fh)


def get_exo_names():
    exo_names_list = []

    for instrument in INSTRUMENTS_LIST:
        for exo in EXO_LIST:
            print("Processing : " + exo['name'])

            ExoClass = exo['class']
            for exo_name in ExoClass.names_list(instrument):
                exo_names_list.append(exo_name)

    return exo_names_list


def get_exo_names_mat():
    exo_names_list = []

    for file in os.listdir(os.path.join(TMQRPATH, "mat")):
        if 'strategy_' in file and '.mat' in file:
            exo_names_list.append(file)

    return exo_names_list



def main():
    # Getting the list of all EXOs / instruments
    #exo_names = get_exo_names_mat()

    logger.info("Starning alpha rebalancer script")

    exo_storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
    exo_names = exo_storage.exo_list()

    for exo in exo_names:
        logger.info("Processing EXO: " + exo)
        # Load alpha modules to process
        for module in os.listdir('alphas'):
            #
            #  Custom EXO folder found
            #
            swm = None
            context = None
            if module == exo.lower() and os.path.isdir(os.path.join('alphas', module)):
                for custom_file in os.listdir(os.path.join('alphas', module)):
                    if 'alpha_' in custom_file and '.py' in custom_file:
                        logger.debug('Processing custom module: ' + os.path.join('alphas', module, custom_file))
                        m = importlib.import_module('scripts.alphas.{0}.{1}'.format(module, custom_file.replace('.py', '')))

                        logger.info('Running CUSTOM alpha: ' + m.STRATEGY_NAME)
                        context = m.STRATEGY_CONTEXT
                        if 'exo_name' in context['strategy'] and context['strategy']['exo_name'] != exo:
                            logger.error("Custom strategy context exo_name != current EXO name (folder mismatch?)")
                            raise ValueError("Custom strategy context exo_name != current EXO name (folder mismatch?)")

                        context['strategy']['exo_name'] = exo
                        context['strategy']['suffix'] = m.STRATEGY_SUFFIX + 'custom'
                        context['strategy']['exo_storage'] = exo_storage

                        swm = Swarm(context)
                        swm.run_swarm()
                        swm.pick()
                        # Saving results to swarms directory
                        swm.save(os.path.join(TMQRPATH, "swarms"))

                        #
                        # Saving last EXO state to online DB
                        #
                        swmonline = SwarmOnlineManager(MONGO_CONNSTR, MONGO_EXO_DB, m.STRATEGY_CONTEXT)
                        swmonline.save(swm)


            # TODO: temporary commented
            elif False: #'alpha_' in module and '.py' in module:
                logger.debug('Processing generic module: ' + module)

                m = importlib.import_module('scripts.alphas.{0}'.format(module.replace('.py','')))
                for direction in [-1, 1]:
                    logger.info('Running alpha: ' + m.STRATEGY_NAME + ' Direction: {0}'.format(direction))
                    context = m.STRATEGY_CONTEXT
                    context['strategy']['exo_name'] = exo
                    context['strategy']['opt_params'][0] = OptParamArray('Direction', [direction])
                    context['strategy']['suffix'] = m.STRATEGY_SUFFIX
                    context['strategy']['exo_storage'] = exo_storage

                    swm = Swarm(context)
                    swm.run_swarm()
                    swm.pick()
                    # Saving results to swarms directory
                    swm.save(os.path.join(TMQRPATH, "swarms"))

                    #
                    # Saving last EXO state to online DB
                    #
                    swmonline = SwarmOnlineManager(MONGO_CONNSTR, MONGO_EXO_DB, m.STRATEGY_CONTEXT)
                    swmonline.save(swm)

if __name__ == '__main__':


    main()
