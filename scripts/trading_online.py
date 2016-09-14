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

from tradingcore.swarmonlinemanager import SwarmOnlineManager
from tradingcore.messages import *
import pprint

class TradingOnlineScript:
    def __init__(self, args, loglevel):
        self.args = args
        self.loglevel = loglevel
        logger = logging.getLogger('TradingOnlineScript')
        logger.setLevel(loglevel)
        fh = None
        if args.logfile != '':
            # create file handler which logs even debug messages
            fh = logging.FileHandler(args.logfile)
            fh.setLevel(loglevel)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(loglevel)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)


        if fh is not None:
            fh.setFormatter(formatter)
            logger.addHandler(fh)

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



    def on_alpha_state_callback(self, appclass, appname, data_object):
        self.log.debug('on_alpha_signal_callback: {0}.{1} Data: {2}'.format(appname, appclass, data_object))
        msg = MsgBase(data_object)

        # Make sure that is valid EXO quote message
        if msg.mtype == MsgAlphaState.mtype:
            self.log.info('Processing Alpha state of: {0} at {1}'.format(msg.swarm_name, msg.last_date))
            # Load EXO structure
            swarm_exposure = msg.exposure
            swarm_prev_exposure = msg.prev_exposure
            swarm_last_date = msg.last_date

            self.log.debug('Swarm Exposure: {0} PrevExposure: {1} LastDate: {2}'.format(swarm_exposure,
                                                                                        swarm_prev_exposure,
                                                                                        swarm_last_date))

            asset_info = self.datasource.assetindex.get_instrument_info(msg.instrument)
            exec_time, decision_time = self.datasource.assetindex.get_exec_time(msg.date, asset_info)

            pos_list = []

            # Get positions composition
            exo_data = self.datasource.exostorage.load_exo(msg.exo_name)
            if exo_data is not None:
                # Generate current swarm net position
                position = Position.from_dict(exo_data['position'], self.datasource, decision_time)
                for contact, pos_dict in position.netpositions.items():
                    pos_list.append(
                        {
                            'ticker': contact.name,
                            'dbid': contact.dbid,
                            'qty': int(pos_dict['qty'] * swarm_exposure)
                        }
                    )
                if self.loglevel == logging.DEBUG:
                    pp = pprint.PrettyPrinter(indent=4)
                    self.log.debug('Current position: \n {0}'.format(pp.pformat(pos_list)))

                # Send position information to real-time software via RabbitMQ
                self.signal_app.send(MsgAlphaSignal(msg, pos_list))

            else:
                self.log.warn("EXO {0} not found in datasource".format(msg.exo_name))



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


    parser.add_argument(
        '-L',
        '--logfile',
        help="Path to logfile",
        action="store",
        default=''
    )


    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    script = TradingOnlineScript(args, loglevel)
    script.main()