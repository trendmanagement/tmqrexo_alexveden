#!/usr/bin/env python
#

# import modules used here -- sys is a very standard one
import sys, argparse, logging
from datetime import datetime, timedelta
import time
import pymongo
from pymongo import MongoClient
from tradingcore.signalapp import SignalApp, APPCLASS_DATA, APPCLASS_EXO

from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.datasource_sql import DataSourceSQL
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.exostorage import EXOStorage

try:
    from .settings import *
except SystemError:
    from scripts.settings import *


class EXOScript:
    def __init__(self, args, loglevel):
        self.signalapp = None
        self.asset_info = None
        self.args = args
        self.loglevel = loglevel

        logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    def check_quote_data(self, appname, appclass, data):
        if appclass != APPCLASS_DATA:
            logging.error("Unexpected APP class message: {0}".format(data))
            return False

        if data is None or len(data) == 0:
            logging.error("Empty message")
            return False
        else:
            if 'date' not in data:
                logging.error("Bad message format")
                return False

        return True

    def get_exo_list(self, args):
        return EXO_LIST

    def on_new_quote(self, appclass, appname, data):
        exec_time, decision_time = self.get_exec_time(datetime.now())

        start_time = time.time()

        print(data)
        print("decision_time: {0}".format(decision_time))

        # Check data integrity
        if not self.check_quote_data(appname, appclass, data):
            return


        quote_date = data['date']
        symbol = appname

        if quote_date >= decision_time:
            # TODO: Check to avoid dupe launch
            # Run first EXO calculation for this day
            logging.info("Run EXO calculation, at decision time")

            assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
            exostorage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

            futures_limit = 3
            options_limit = 10

            #datasource = DataSourceMongo(mongo_connstr, mongo_db_name, assetindex, futures_limit, options_limit, exostorage)
            datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, assetindex, futures_limit, options_limit, exostorage)

            # Run EXO calculation
            self.run_exo_calc(datasource, decision_time, symbol, isbackfill=False)

            end_time = time.time()
            # TODO: textlog status
            self.signalapp.send(self.signalapp.status('OK', 'EXO Processed', context={'instrument': symbol, 'date': quote_date, 'exec_time': end_time-start_time}))




        else:
            logging.debug("Waiting next decision time")

    def get_exec_time(self, dt):
        exec_time = datetime.combine(dt.date(), self.asset_info["customdayboundarytime"].time())
        decision_time = datetime.combine(dt.date(), self.asset_info["customdayboundarytime"].time()) - timedelta(minutes=self.asset_info["decisionoffsetminutes"])
        return exec_time, decision_time

    def run_exo_calc(self, datasource, decision_time, symbol, isbackfill):
        # Running all EXOs builder algos
        exos_list = self.get_exo_list(args)
        for exo in exos_list:
            logging.info('Processing EXO: {0} at {1}'.format(exo['name'], decision_time))

            ExoClass = exo['class']

            # Processing Long/Short and bidirectional EXOs
            for direction in [1, -1]:
                if ExoClass.direction_type() == 0 or ExoClass.direction_type() == direction:
                    with ExoClass(symbol, direction, decision_time, datasource, log_file_path=args.debug) as exo_engine:
                        logging.debug("Running EXO instance: " + exo_engine.name)
                        # Load EXO information from mongo
                        exo_engine.load()
                        exo_engine.calculate()
                        if not isbackfill:
                            # TODO: Send signal to alphas that EXO price is ready
                            pass

    def do_backfill(self):
        #
        logging.info("Run EXO backfill from {0}".format(self.args.backfill))

        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        exostorage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

        futures_limit = 3
        options_limit = 10
        # datasource = DataSourceMongo(mongo_connstr, mongo_db_name, assetindex, futures_limit, options_limit, exostorage)
        datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, assetindex, futures_limit, options_limit, exostorage)

        exec_time, decision_time = self.get_exec_time(self.args.backfill)

        exec_time_end, decision_time_end = self.get_exec_time(datetime.now())
        # TODO: before calculation we need to do rollback of old transactions (to maintain EXO granularity)

        while decision_time <= decision_time_end:
            logging.info("Backfilling: {0}".format(decision_time))

            self.run_exo_calc(datasource, decision_time, args.instrument, isbackfill=True)

            decision_time += timedelta(days=1)
            exec_time += timedelta(days=1)


    def main(self):
        logging.info("Initiating EXO building engine")

        # Initialize EXO engine SignalApp (report first status)
        self.signalapp = SignalApp(self.args.instrument, APPCLASS_EXO, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)
        self.signalapp.send(self.signalapp.status('INIT', 'Initiating EXO engine'))

        # Get information about decision and execution time
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        self.asset_info = assetindex.get_instrument_info(args.instrument)


        if self.args.backfill is not None:
            # Backfill mode enabled
            self.do_backfill()
        else:
            # Online mode

            # Subscribe to datafeed signal app
            logging.debug('Subscribing datafeed for: ' + self.args.instrument)
            datafeed = SignalApp(self.args.instrument, APPCLASS_DATA, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)
            # Listening datafeed loop
            datafeed.listen(self.on_new_quote)




# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="EXO generation batch script",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")


    parser.add_argument(
        "-E",
        "--exolist",
        help="List of EXO products to calculate default: %(default)s",
        action="append",
        default='*')


    parser.add_argument(
        '-D',
        '--debug',
        help="Debug log files folder path if set",
        action="store",
        default=''
    )


    def valid_date(s):
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

    parser.add_argument(
        '-B',
        '--backfill',
        help="Backfill EXO data from date YYYY-MM-DD",
        action="store", type=valid_date
    )

    parser.add_argument('instrument', type=str,
                        help='instrument name for EXO')



    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    script = EXOScript(args, loglevel)
    script.main()