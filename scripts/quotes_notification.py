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
import holidays
import bdateutil

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


NULL_DATE = datetime(1900, 1, 1, 0, 0, 0)


class QuotesNotifyScript:
    def __init__(self, args, loglevel):
        self.signalapp = None
        self.asset_info = None
        self.args = args
        self.loglevel = loglevel
        self.last_quote_date = None
        self.last_minute = -1
        logging.getLogger("pika").setLevel(logging.WARNING)
        logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=loglevel)
        self.pprinter = pprint.PrettyPrinter(indent=4)



    def get_last_quote_date(self):
        document = self.status_db[STATUS_QUOTES_COLLECTION].find_one({'instrument': self.args.instrument})
        if document is not None and 'last_bar_time' in document:
            return document['last_bar_time']
        else:
            return NULL_DATE


    def set_last_quote_state(self, context, update):
        if not update:
            self.status_db[STATUS_QUOTES_COLLECTION].replace_one({'instrument': context['instrument']}, context, upsert=True)
        else:
            self.status_db[STATUS_QUOTES_COLLECTION].update_one({'instrument': context['instrument']}, {
                '$set': {
                    'last_bar_time': context['last_bar_time'],
                    'now': context['now'],
                    'quote_status': context['quote_status']
                }
            })


    def get_last_bar_time(self):
        last_bar_time = self.db['futurebarcol'].find({'errorbar': False}).sort('bartime', pymongo.DESCENDING).limit(1).next()['bartime']
        return last_bar_time

    def date_now(self):
        return datetime.now()

    def main(self):
        logging.info("Initiating data notification script")

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
        self.db = client[mongo_db_name]
        # Creating index for 'bartime'
        self.db['futurebarcol'].create_index([('bartime', pymongo.DESCENDING)], background=True)

        status_client = MongoClient(MONGO_CONNSTR)
        self.status_db = status_client[MONGO_EXO_DB]
        self.status_db[STATUS_QUOTES_COLLECTION].create_index([('instrument', pymongo.DESCENDING)], background=True)

        last_minute = 0
        while True:
            # Getting last bar time from DB
            last_bar_time = self.get_last_bar_time()
            self.process_quote(last_bar_time)
            time.sleep(15)

    def is_quote_delayed(self, last_bar_time):
        dtnow = self.date_now()
        if bdateutil.isbday(dtnow, holidays=holidays.US()) and dtnow.hour > 8 and dtnow.hour < 13:
            if int(abs((dtnow-last_bar_time).total_seconds() / 60.0)) > self.args.delay:
                return True

        return False

    def process_quote(self, last_bar_time):
        dtnow = self.date_now()

        exec_time, decision_time = AssetIndexMongo.get_exec_time(dtnow, self.asset_info)
        if self.last_quote_date is None:
            self.last_quote_date = self.get_last_quote_date()

        quote_status = 'IDLE'

        if self.is_quote_delayed(last_bar_time):
            if self.last_minute != dtnow.minute:
                logging.info('Quote delayed more than {0} minutes '
                             'for {1} LastBarTimeDB: {2} Now: {3}'.format(self.args.delay,
                                                                          self.args.instrument,
                                                                          last_bar_time,
                                                                          dtnow))

                self.signalapp.send(MsgStatus('DELAY',
                                              'Quote delayed more than {0} minutes '
                                              'for {1} LastBarTimeDB: {2} Now: {3}'.format(self.args.delay,
                                                                                           self.args.instrument,
                                                                                           last_bar_time,
                                                                                           dtnow)))
                quote_status = 'DELAY'
        logging.info('Running new bar. Bar time: {0}'.format(last_bar_time))

        # Fire new quote notification if last_bar_time > decision_time
        if self.last_quote_date.date() != last_bar_time.date() and last_bar_time > decision_time:
            if quote_status != 'DELAY':
                quote_status = 'RUN'
            # Reporting current status
            self.signalapp.send(MsgStatus('RUN', 'Processing new bar {0}'.format(last_bar_time)))
            logging.info('Running new bar. Bar time: {0}'.format(last_bar_time))
            self.last_quote_date = last_bar_time
            context = {
                'last_bar_time': last_bar_time,
                'now': dtnow,
                'last_run_date': self.last_quote_date,
                'decision_time': decision_time,
                'execution_time': exec_time,
                'instrument': self.args.instrument,
                'quote_status': quote_status,
            }
            logging.debug('Current context:\n {0}'.format(self.pprinter.pformat(context)))
            self.signalapp.send(MsgQuoteNotification(self.args.instrument, last_bar_time, context))
            self.set_last_quote_state(context, update=False)

        else:
            context = {
                'last_bar_time': last_bar_time,
                'now': dtnow,
                'last_run_date': self.last_quote_date,
                'decision_time': decision_time,
                'execution_time': exec_time,
                'instrument': self.args.instrument,
                'quote_status': quote_status,
            }

            if self.last_quote_date == NULL_DATE:
                # If quote is absent is status_quotes collection, insert new
                self.set_last_quote_state(context, update=False)
            else:
                self.set_last_quote_state(context, update=True)

            # Log initial information:
            if self.last_minute == -1:
                logging.debug('Current context:\n {0}'.format(self.pprinter.pformat(context)))
            elif self.last_minute != dtnow.minute:
                logging.debug('Last bar time {0}'.format(last_bar_time))

            self.last_minute = dtnow.minute
            self.signalapp.send(MsgStatus('IDLE', 'Last bar time {0}'.format(last_bar_time), context))


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

    parser.add_argument(
        "-D",
        "--delay",
        help="Delay warning interval in minutes default: %(default)s minutes",
        action="store",
        default=3)


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