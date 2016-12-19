"""
Online alpha execution script for custom alphas (calculated for only particular EXO)

"""

# import modules used here -- sys is a very standard one
import sys, argparse, logging
from tradingcore.signalapp import SignalApp, APPCLASS_ALPHA, APPCLASS_EXO
import os

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


class AlphaOnlineScript:
    def __init__(self, args, loglevel):
        self.args = args
        self.loglevel = loglevel
        self.custom_exo = args.exoname
        logging.getLogger("pika").setLevel(logging.WARNING)
        logger = logging.getLogger('AlphaCustomOnlineScript')
        logger.setLevel(loglevel)

        # create console handler with a higher log level
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(loglevel)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)


        self.log = logger

        self.log.info('Init AlphaCustomOnlineScript CusomEXO: {0}'.format(self.custom_exo))

        self.signal_app = SignalApp('CustomAlpha_'+self.custom_exo, APPCLASS_ALPHA, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)
        self.signal_app.send(MsgStatus("INIT", 'Initiating online alpha custom engine {0}'.format(self.custom_exo)))
        self.exo_app = SignalApp('*', APPCLASS_EXO, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)



    def swarm_updated_callback(self, swm):
        # Logging swarm structure information
        if self.loglevel == logging.DEBUG:
            self.log.debug('swarm_updated_callback: Swarm processed: {0}'.format(swm.name))
            last_state = swm.laststate_to_dict()
            del last_state['swarm_series']
            pp = pprint.PrettyPrinter(indent=4)

            self.log.debug('Swarm last state: \n {0}'.format(pp.pformat(last_state)))

        self.signal_app.send(MsgAlphaState(swm))

    def on_exo_quote_callback(self, appclass, appname, msg):

        # Make sure that is valid EXO quote message
        if msg.mtype == MsgEXOQuote.mtype:
            module = msg.exo_name.lower()
            if module == self.args.exoname.lower():
                self.log.debug('on_exo_quote_callback: {0}.{1} Data: {2}'.format(appname, appclass, data_object))
                if os.path.isdir(os.path.join('alphas', module)):
                    self.log.info('Processing EXO quote: {0} at {1}'.format(msg.exo_name, msg.exo_date))
                    for custom_file in os.listdir(os.path.join('alphas', module)):
                        if 'alpha_' in custom_file and '.py' in custom_file:
                            self.log.info('Running alpha strategy from: {0}'.format(os.path.join('alphas', module, custom_file)))
                            try:
                                # Load strategy_context
                                m = importlib.import_module(
                                    'scripts.alphas.{0}.{1}'.format(module, custom_file.replace('.py', '')))

                                # Initiate swarm from Mongo DB
                                exo_name = msg.exo_name

                                context = m.STRATEGY_CONTEXT
                                context['strategy']['suffix'] = m.STRATEGY_SUFFIX + 'custom'

                                swmonline = SwarmOnlineManager(MONGO_CONNSTR, MONGO_EXO_DB, context)
                                # Update and save swarm with new day data (and run callback)
                                swmonline.process(exo_name, swm_callback=self.swarm_updated_callback)
                            except:
                                self.log.exception("Failed to process EXO quote: {0}".format(msg.exo_name))

    def main(self):
        """
        Application main()
        :return:
        """
        # Subscribe to rabbit MQ EXO feed
        self.exo_app.listen(self.on_exo_quote_callback)



# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="EXO Alpha online script",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")




    parser.add_argument('exoname', type=str,
                        help='Custom EXO module name (see ./alphas/{CUSTOM_EXO}/*.py files list)')



    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    script = AlphaOnlineScript(args, loglevel)
    script.main()



