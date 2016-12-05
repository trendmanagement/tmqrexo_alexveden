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


import os, sys
import importlib
from backtester.swarms.swarm import Swarm
from backtester.strategy import OptParamArray
from exobuilder.data.exostorage import EXOStorage
from tradingcore.swarmonlinemanager import SwarmOnlineManager

# import modules used here -- sys is a very standard one
import sys, argparse, logging


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

def run_custom(args, exo_storage):
    logging.debug('Processing custom module: ' + args.alpha_file)
    package_path = args.alpha_file.replace('/','.').replace('.py','')
    importlib.invalidate_caches()

    try:
        m = importlib.import_module(package_path)
    except:
        logging.error("Module not found: "+package_path)
        sys.exit(2)

    logging.info('Running CUSTOM alpha: ' + Swarm.get_name(m.STRATEGY_CONTEXT, m.STRATEGY_SUFFIX))
    context = m.STRATEGY_CONTEXT
    context['strategy']['suffix'] = m.STRATEGY_SUFFIX + 'custom'
    context['strategy']['exo_storage'] = exo_storage

    try:
        if 'exo_name' in context['strategy'] and context['strategy']['exo_name'].lower() not in args.alpha_file:
            logging.error("Custom strategy context exo_name != current EXO name (folder mismatch?)")
            raise ValueError("Custom strategy context exo_name != current EXO name (folder mismatch?)")

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
        logging.exception("Exception occurred:")
        sys.exit(-1)


def main(args, loglevel):
    if args.logfile == '':
        logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=loglevel)
    else:
        logging.basicConfig(filename=args.logfile, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=loglevel)

    #exo_names = get_exo_names_mat()
    logging.info("Starting...")
    exo_storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

    if args.generic:
        exo_names = exo_storage.exo_list()
        # Run alpha code for all EXOs
        raise NotImplementedError("Genering alpha not supported yet")
    else:
        # Run custom alpha module
        run_custom(args, exo_storage)

    logging.info("Done.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Single alpha strategy backtesting script",
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

    parser.add_argument(
        "-G",
        "--generic",
        help="Run generic alpha script for all EXOs",
        action="store_true",
        default=False)

    parser.add_argument('alpha_file', type=str,
                        help='Path to alpha file')

    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
