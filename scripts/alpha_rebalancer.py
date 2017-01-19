"""
This script used for scheduled alpha execution over weekend

How it works:

1. Run every alpha for every EXO
2. Run swarm optimization routine
3. Rebalance new swarms set
4. Save new swarm composition to MongoDB
"""
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

from scripts.settings_exo import *
import importlib
import os

from backtester.strategy import OptParamArray
from backtester.swarms.swarm import Swarm
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.exostorage import EXOStorage
from tradingcore.execution_manager import ExecutionManager
from tradingcore.swarmonlinemanager import SwarmOnlineManager

# import modules used here -- sys is a very standard one
import sys, argparse, logging
from tradingcore.messages import *
from tradingcore.signalapp import SignalApp, APPCLASS_ALPHA
from datetime import datetime


TMQRPATH = os.getenv("TMQRPATH", '')


#
# Handling unexpected exceptions
#
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception


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

def get_alpha_modules(base_dir, exo_names):
    results = {}
    os.chdir(base_dir)
    for exo in exo_names:
        alphas_list = results.setdefault(exo, {})
        for module in os.listdir('alphas'):
            if module == exo.lower() and os.path.isdir(os.path.join('alphas', module)):
                for custom_file in os.listdir(os.path.join('alphas', module)):
                    if 'alpha_' in custom_file and '.py' in custom_file:
                        module_name = 'scripts.alphas.{0}.{1}'.format(module, custom_file.replace('.py', ''))
                        alphas_list[module_name] = {'custom': True}
            elif 'alpha_' in module and '.py' in module:
                module_name = 'scripts.alphas.{0}'.format(module.replace('.py',''))
                alphas_list[module_name] = {'custom': False}

    return results




def main(args, loglevel):
    if args.logfile == '':
        logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=loglevel)
    else:
        logging.basicConfig(filename=args.logfile, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=loglevel)
    signalapp = SignalApp("AlphaRebalancer", APPCLASS_ALPHA, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)
    signalapp.send(MsgStatus('INIT', 'Initiating alpha rebalancer script'))

    #exo_names = get_exo_names_mat()
    logging.getLogger("pika").setLevel(logging.WARNING)
    logging.info("Starting...")

    exo_storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
    exo_names = exo_storage.exo_list()

    for exo in exo_names:
        logging.info("Processing EXO: " + exo)

        # Check for EXO data validity
        exo_df, exo_info = exo_storage.load_series(exo)
        if len(exo_df) == 0 or len(exo_df) < 200 or (datetime.now() - exo_df.index[-1]).days < 4:
            logging.error("Not actual EXO data found in {0} last date: \n{1}".format(exo, exo_df.tail()))
            last_exo_date = 'N/A' if len(exo_df) == 0 else exo_df.index[-1]
            signalapp.send(MsgStatus('ERROR',
                                     'Not actual or empty EXO data found in {0} last date {1}'.format(exo, last_exo_date),
                                     notify=True))
            break

        # Load alpha modules to process
        for module in os.listdir('alphas'):
            #
            #  Custom EXO folder found
            #
            swm = None
            context = None

            if module.lower() == exo.lower() and os.path.isdir(os.path.join('alphas', module)):
                for custom_file in os.listdir(os.path.join('alphas', module)):
                    if 'alpha_' in custom_file and '.py' in custom_file:
                        logging.debug('Processing custom module: ' + os.path.join('alphas', module, custom_file))
                        try:
                            m = importlib.import_module('scripts.alphas.{0}.{1}'.format(module, custom_file.replace('.py', '')))

                            context = m.STRATEGY_CONTEXT
                            context['strategy']['exo_name'] = exo
                            context['strategy']['suffix'] = m.STRATEGY_SUFFIX + 'custom'
                            context['strategy']['exo_storage'] = exo_storage

                            logging.info('Running CUSTOM alpha: ' + Swarm.get_name(m.STRATEGY_CONTEXT, m.STRATEGY_SUFFIX))

                            if 'exo_name' in context['strategy'] and context['strategy']['exo_name'] != exo:
                                logging.error("Custom strategy context exo_name != current EXO name (folder mismatch?)")
                                raise ValueError(
                                    "Custom strategy context exo_name != current EXO name (folder mismatch?)")

                            swm = Swarm(context)
                            swm.run_swarm()
                            swm.pick()

                            #
                            # Saving last EXO state to online DB
                            #

                            swmonline = SwarmOnlineManager(MONGO_CONNSTR, MONGO_EXO_DB, m.STRATEGY_CONTEXT)
                            logging.debug('Saving: {0}'.format(swm.name))
                            swmonline.save(swm)

                        except:
                            logging.exception('Exception occurred:')
                            signalapp.send(MsgStatus('ERROR',
                                                     'Exception in {0}'.format(
                                                         Swarm.get_name(m.STRATEGY_CONTEXT, m.STRATEGY_SUFFIX)),
                                                     notify=True))

            elif 'alpha_' in module and '.py' in module:
                logging.debug('Processing generic module: ' + module)
                try:
                    m = importlib.import_module('scripts.alphas.{0}'.format(module.replace('.py','')))
                    for direction in [-1, 1]:
                        context = m.STRATEGY_CONTEXT
                        context['strategy']['exo_name'] = exo
                        context['strategy']['opt_params'][0] = OptParamArray('Direction', [direction])
                        context['strategy']['suffix'] = m.STRATEGY_SUFFIX
                        context['strategy']['exo_storage'] = exo_storage

                        logging.info('Running alpha: ' + Swarm.get_name(m.STRATEGY_CONTEXT) + ' Direction: {0}'.format(direction))


                        swm = Swarm(context)
                        swm.run_swarm()
                        swm.pick()
                        #
                        # Saving last EXO state to online DB
                        #
                        swmonline = SwarmOnlineManager(MONGO_CONNSTR, MONGO_EXO_DB, m.STRATEGY_CONTEXT)
                        logging.debug('Saving: {0}'.format(swm.name))
                        swmonline.save(swm)
                except Exception as exc:
                    logging.exception('Exception occurred:')
                    signalapp.send(MsgStatus('ERROR',
                                             'Exception in {0} Message: {1}'.format(
                                                 Swarm.get_name(m.STRATEGY_CONTEXT, m.STRATEGY_SUFFIX),
                                                 exc,
                                             ),
                                             notify=True))

    logging.info("Processing accounts positions")
    assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
    datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, futures_limit=10, options_limit=10,
                                 exostorage=exo_storage)
    exmgr = ExecutionManager(MONGO_CONNSTR, datasource, dbname=MONGO_EXO_DB)
    exmgr.account_positions_process(write_to_db=True)

    signalapp.send(MsgStatus('RUN', 'Alpha rebalancer script', notify=True))
    logging.info("Done.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Bulk alpha strategy backtesting script",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")

    parser.add_argument(
        "-L",
        "--logfile",
        help="Log file path",
        action="store",
        default='')

    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
