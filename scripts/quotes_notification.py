#!/usr/bin/env python
"""
Quotes notification script

Used in online trading setup, checks if last bar time of the last quote for particular instrument > decision time fires
``new_quote`` event to RabbitMQ and launches full execution chain NewQuote -> ExoCalculation -> NewEXOQuote -> AlphaCalcultation -> PositionQtyUpdate

Poll interval: 15 secs
"""

# import modules used here -- sys is a very standard one
import sys, argparse, logging
from datetime import datetime, timedelta, date
import time
import pymongo
from pymongo import MongoClient
from tradingcore.signalapp import SignalApp, APPCLASS_DATA
from tradingcore.messages import *
from exobuilder.data.assetindex_mongo import AssetIndexMongo
import pprint

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


class QuotesNotifyScript:
    def __init__(self, args, loglevel):
        self.signalapp = None
        self.asset_info = None
        self.args = args
        self.loglevel = loglevel
        self.last_quote_date = date(2000, 1, 1)
        self.last_minute = -1
        logging.getLogger("pika").setLevel(logging.WARNING)
        logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=loglevel)

    def get_last_bar_time(self, db):
        last_bar_time = db['futurebarcol'].find({'errorbar': False}).sort('bartime', pymongo.DESCENDING).limit(1).next()['bartime']
        return last_bar_time

    def main(self):
        logging.info("Initiating EXO building engine")

        # Initialize EXO engine SignalApp (report first status)
        self.signalapp = SignalApp(self.args.instrument, APPCLASS_DATA, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)
        self.signalapp.send(MsgStatus('INIT', 'Initiating data notification script'))

        # Get information about decision and execution time
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        self.asset_info = assetindex.get_instrument_info(args.instrument)


        # TODO: replace DB name after release
        mongo_db_name = 'tmldb_test'
        tmp_mongo_connstr = 'mongodb://tml:tml@10.0.1.2/tmldb_test?authMechanism=SCRAM-SHA-1'
        client = MongoClient(tmp_mongo_connstr)
        db = client[mongo_db_name]
        pp = pprint.PrettyPrinter(indent=4)

        #
        # Creating index for 'bartime'
        #
        db['futurebarcol'].create_index([('bartime', pymongo.DESCENDING)], background=True)

        while True:
            # Getting last bar time from DB
            last_bar_time = self.get_last_bar_time(db)
            exec_time, decision_time = AssetIndexMongo.get_exec_time(datetime.now(), self.asset_info)



            # Fire new quote notification if last_bar_time > decision_time
            if self.last_quote_date != last_bar_time.date() and last_bar_time > decision_time:
                # Reporting current status
                self.signalapp.send(MsgStatus('RUN', 'Processing new bar {0}'.format(last_bar_time)))
                logging.info('Running new bar. Bar time: {0}'.format(last_bar_time))

                context = {
                    'last_bar_time': last_bar_time,
                    'now': datetime.now(),
                    'last_run_date': self.last_quote_date,
                    'decision_time': decision_time,
                    'execution_time': exec_time,
                    'instrument': self.args.instrument,
                }
                logging.debug('Current context:\n {0}'.format(pp.pformat(context)))
                self.signalapp.send(MsgQuoteNotification(self.args.instrument, last_bar_time, context))
                self.last_quote_date = last_bar_time.date()
            else:
                dtnow = datetime.now()
                context = {
                    'last_bar_time': last_bar_time,
                    'now': dtnow,
                    'last_run_date': self.last_quote_date,
                    'decision_time': decision_time,
                    'execution_time': exec_time,
                    'instrument': self.args.instrument,
                }

                # Log initial information:
                if self.last_minute == -1:
                    logging.debug('Current context:\n {0}'.format(pp.pformat(context)))
                elif self.last_minute != dtnow.minute:
                    logging.debug('Last bar time {0}'.format(last_bar_time))

                self.last_minute = dtnow.minute
                self.signalapp.send(MsgStatus('IDLE', 'Last bar time {0}'.format(last_bar_time), context))
            time.sleep(15)




# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Simple quotes notification script",
        epilog="Runs every 15 seconds and reads MongoDB collection for new quotes.",
        fromfile_prefix_chars='@')

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")


    parser.add_argument('instrument', type=str,
                        help='instrument name for EXO')



    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    script = QuotesNotifyScript(args, loglevel)
    script.main()