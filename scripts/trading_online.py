"""
Calculates account positions after some of alphas is calculated
"""
# import modules used here -- sys is a very standard one
import sys, argparse, logging
from tradingcore.signalapp import SignalApp, APPCLASS_ALPHA, APPCLASS_SIGNALS
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.exostorage import EXOStorage
from exobuilder.data.datasource import DataSourceBase
from exobuilder.exo.position import Position

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
import importlib

from tradingcore.execution_manager import ExecutionManager
from tradingcore.messages import *
import pprint

class TradingOnlineScript:
    def __init__(self, args, loglevel):
        self.args = args
        self.loglevel = loglevel
        logging.getLogger("pika").setLevel(logging.WARNING)
        logger = logging.getLogger('TradingOnlineScript')
        logger.setLevel(loglevel)

        # create console handler with a higher log level
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(loglevel)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        self.log = logger

        self.log.info('Init TradingOnlineScript')

        self.signal_app = SignalApp('TradingOnlineScript', APPCLASS_SIGNALS, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)
        self.signal_app.send(MsgStatus("INIT", 'Initiating trading online engine'))
        self.alpha_app = SignalApp('*', APPCLASS_ALPHA, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)

        #
        # Init EXO engine datasource
        #
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        exostorage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

        futures_limit = 3
        options_limit = 10
        self.datasource = DataSourceBase(assetindex, futures_limit, options_limit, exostorage)

        self.exmgr = ExecutionManager(MONGO_CONNSTR, self.datasource, MONGO_EXO_DB)



    def on_alpha_state_callback(self, appclass, appname, msg):

        # Make sure that is valid EXO quote message
        if msg.mtype == MsgAlphaState.mtype:
            self.log.debug('on_alpha_signal_callback: {0}.{1} Data: {2}'.format(appname, appclass, msg))
            self.log.info('Processing Alpha state of: {0} at {1}'.format(msg.swarm_name, msg.last_date))
            try:
                # Processing positions for each campaign/account
                pos_list = self.exmgr.account_positions_process(write_to_db=True)
                pp = pprint.PrettyPrinter(indent=4)
                self.log.debug(pp.pformat(pos_list))

                # Send position information to real-time software via RabbitMQ
                self.signal_app.send(MsgAlphaSignal(msg, pos_list))
            except:
                self.log.exception("Error in processing account positions")


    def main(self):
        """
        Application main()
        :return:
        """
        # Subscribe to rabbit MQ EXO feed
        self.alpha_app.listen(self.on_alpha_state_callback)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Trading orders management online script",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")


    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    script = TradingOnlineScript(args, loglevel)
    script.main()