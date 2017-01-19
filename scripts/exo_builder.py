#!/usr/bin/env python
"""
``scripts/exo_builder.py`` is a main script for EXO historical backfill and online management, using command line arguments you can use this script in 2 modes:
    * **backfill mode** - used for EXO historical price building and backfilling
    * **online mode** - used for online EXO data processing on current date

One ``exo_builder.py`` instance run for each product required

Script usage:

.. code-block:: none

    usage: exo_builder.py [-h] [-v] [-E EXOLIST] [-D DEBUG] [-B BACKFILL]
                      instrument

    EXO generation batch script

    positional arguments:
      instrument            instrument name for EXO

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         increase output verbosity
      -E EXOLIST, --exolist EXOLIST
                            List of EXO products to calculate default: *
      -D DEBUG, --debug DEBUG
                            Debug log files folder path if set
      -B BACKFILL, --backfill BACKFILL
                            Backfill EXO data from date YYYY-MM-DD

    As an alternative to the commandline, params can be placed in a file, one per
    line, and specified on the commandline like 'exo_builder.py @params.conf'.


By default ``exo_builder.py`` uses EXO list stored in constant ``EXO_LIST`` in ``scripts/settings.py``

Brief algorithm of work (in ``backfill`` mode):

1. Load information about defined product (i.e. ``instrument`` positional argument)
2. Load EXO settings from ``scripts/settings.py``
3. For each day in period between starting date (i.e. --backfill YYYY-MM-DD argument) and Date.Now
    * Load and initiate EXO class instance
    * Calculate EXO position
    * Store EXO values for particular date
    * Loop to next date

In **online mode** ``exo_builder.py`` is calculated only for current date and sends signal to RabbitMQ about EXO calculation finished.
"""

#

# import modules used here -- sys is a very standard one
import argparse
import logging
import sys
import time
from datetime import timedelta

from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.datasource_hybrid import DataSourceHybrid
from exobuilder.data.datasource_sql import DataSourceSQL
from exobuilder.data.exostorage import EXOStorage
from tradingcore.messages import *
from tradingcore.signalapp import SignalApp, APPCLASS_DATA, APPCLASS_EXO
import warnings
from scripts.settings_exo import *
import bdateutil
import holidays
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


class EXOScript:
    def __init__(self, args, loglevel):
        self.signalapp = None
        self.asset_info = None
        self.args = args
        self.loglevel = loglevel
        logging.getLogger("pika").setLevel(logging.WARNING)

        self.logger = logging.getLogger('EXOBuilder')
        self.logger.setLevel(loglevel)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # create console handler with a higher log level
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        if self.args.logfile != '':
            if os.path.exists(os.path.dirname(self.args.logfile)):
                fh = logging.FileHandler(self.args.logfile, mode='w')
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)
            else:
                self.logger.error("Can't find logfile path in {0}".format(self.args.logfile))


    def check_quote_data(self, appname, appclass, data):
        if appclass != APPCLASS_DATA:
            self.logger.error("Unexpected APP class message: {0}".format(data))
            return False

        if data is None:
            self.logger.error("Empty message")
            return False
        return True

    def check_bday_or_holiday(self, date):
        if date.weekday() >= 5 or not bdateutil.isbday(date, holidays=holidays.US()):
            # Skipping weekends and US holidays
            # date.weekday() >= 5 - 5 is Saturday!
            return False

        return True

    def get_exo_list(self, args):
        if args.exolist == "*":
            return EXO_LIST
        else:
            self.logger.debug("Processing list of EXOs: "+args.exolist)
            result = []
            list_set = {}
            for e in args.exolist.split(','):
                # Avoid duplicates
                if e.lower() not in list_set:
                    for exo_setts in EXO_LIST:
                        if exo_setts['name'].lower() == e.lower():
                            list_set[e.lower()] = exo_setts
                            result.append(exo_setts)
            if len(result) == 0:
                raise ValueError("EXO list is empty, bad filter? ({0})".format(args.exolist))


            return result


    def on_new_quote(self, appclass, appname, data):
        if data.mtype != MsgQuoteNotification.mtype:
            return

        # Check data integrity
        if not self.check_quote_data(appname, appclass, data):
            self.logger.warning("Quote signal message integrity checks failed")
            self.logger.warning("AppName: {0} AppClass: {1} MsgData: {2}".format(appname, appclass, data))

            self.signalapp.send(MsgStatus('ERROR',
                                          'Quote signal message integrity checks failed. Check logs...',
                                          notify=True
                                          )
                                )
            return


        exec_time, decision_time = AssetIndexMongo.get_exec_time(datetime.now(), self.asset_info)
        start_time = time.time()

        if not self.check_bday_or_holiday(exec_time):
            self.logger.warning("Skipping EXO quote calculation due to weekend or holiday")

            self.signalapp.send(MsgStatus('SKIPPED',
                                          'Skipping EXO quote calculation due to weekend or holiday',
                                          notify=True
                                          )
                                )
            return

        quote_date = data.date
        symbol = appname

        if quote_date >= decision_time:
            # TODO: Check to avoid dupe launch
            # Run first EXO calculation for this day
            self.logger.info("Run EXO calculation, at decision time: {0}".format(decision_time))

            assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
            exostorage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)



            futures_limit = 3
            options_limit = 20

            #datasource = DataSourceMongo(mongo_connstr, mongo_db_name, assetindex, futures_limit, options_limit, exostorage)
            #datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, assetindex, futures_limit, options_limit, exostorage)
            #
            # Test DB temporary credentials
            #
            tmp_mongo_connstr = 'mongodb://tml:tml@10.0.1.2/tmldb_test?authMechanism=SCRAM-SHA-1'
            tmp_mongo_db = 'tmldb_test'
            datasource = DataSourceHybrid(SQL_HOST, SQL_USER, SQL_PASS, assetindex, tmp_mongo_connstr, tmp_mongo_db,
                                          futures_limit, options_limit, exostorage)

            # Run EXO calculation
            self.run_exo_calc(datasource, decision_time, symbol, backfill_dict=None)

            end_time = time.time()
            self.signalapp.send(MsgStatus('RUN',
                                          'EXOs processed for {0} at {1} (CalcTime: {2:0.2f}s)'.format(symbol, quote_date, end_time-start_time),
                                          context={'instrument': symbol,
                                                   'date': quote_date,
                                                   'exec_time': end_time-start_time},
                                          notify=True
                                          )
                                )

        else:
            self.signalapp.send(MsgStatus('SKIPPED',
                                          'EXO calculation skipped for {0} at {1}, quote date < decision_time'.format(symbol, quote_date),
                                          notify=True
                                          )
                                )
            self.logger.debug("Waiting next decision time")



    def run_exo_calc(self, datasource, decision_time, symbol, backfill_dict):
        # Running all EXOs builder algos
        exos_list = self.get_exo_list(args)

        for exo in exos_list:
            self.logger.info('Processing EXO: {0} at {1}'.format(exo['name'], decision_time))

            ExoClass = exo['class']

            # Processing Long/Short and bidirectional EXOs
            for direction in [1, -1]:
                if ExoClass.direction_type() == 0 or ExoClass.direction_type() == direction:
                    try:
                        with ExoClass(symbol, direction, decision_time, datasource, log_file_path=args.debug) as exo_engine:
                            try:
                                asset_list = exo_engine.ASSET_LIST
                                # Checking if current symbol is present in EXO class ASSET_LIST
                                if asset_list is not None:
                                    if symbol not in asset_list:
                                        # Skipping assets which are not in the list
                                        continue
                            except AttributeError:
                                warnings.warn("EXO class {0} doesn't contain ASSET_LIST attribute filter, calculating all assets".format(ExoClass))

                            if backfill_dict is not None:
                                #
                                # Check if last EXO quote is < decision_time
                                #   if True - skip the calculation until actual date come
                                #
                                # Note: this is fix for situations when we added new EXO, and we need it to be calculated
                                #  from the beginning of the history
                                if exo_engine.exo_name in backfill_dict:
                                    exo_start_date = backfill_dict[exo_engine.exo_name]
                                    if decision_time < exo_start_date:
                                        break


                            self.logger.debug("Running EXO instance: " + exo_engine.name)
                            # Load EXO information from mongo
                            exo_engine.load()
                            if backfill_dict is None:
                                #
                                # Check quotes lengths in Online mode (prevent filling by recent quotes unbackfilled EXOs)
                                #
                                if len(exo_engine.series) == 0 or (datetime.now() - exo_engine.series.index[-1]).days > 7:
                                    self.logger.exception("EXO backfill required: {0} on {1}".format(ExoClass, symbol))
                                    self.signalapp.send(MsgStatus("ERROR",
                                                                  "EXO backfill required: {0}".format(exo_engine.name),
                                                                  notify=True)
                                                        )
                                    continue

                            exo_engine.calculate()
                            if backfill_dict is None:
                                # Sending signal to alphas that EXO price is ready
                                self.signalapp.send(MsgEXOQuote(exo_engine.exo_name, decision_time))
                    except Exception as exc:
                        self.logger.exception("Failed processing EXO: {0} on {1}".format(ExoClass, symbol))
                        self.signalapp.send(MsgStatus("ERROR",
                                                      "Failed processing EXO: {0} on {1} Reason: {2}".format(ExoClass,
                                                                                                             symbol,
                                                                                                             exc),
                                                      notify=True)
                                            )



    def do_backfill(self):
        #
        self.logger.info("Run EXO backfill from {0}".format(self.args.backfill))

        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        exostorage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

        futures_limit = 3
        options_limit = 20
        # datasource = DataSourceMongo(mongo_connstr, mongo_db_name, assetindex, futures_limit, options_limit, exostorage)
        datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, assetindex, futures_limit, options_limit, exostorage)

        exos = exostorage.exo_list(exo_filter=self.args.instrument+'_', return_names=True)

        exo_start_dates = {}
        exec_time, decision_time = AssetIndexMongo.get_exec_time(self.args.backfill, self.asset_info)

        current_time = decision_time

        if len(exos) > 0:
            for exo_name in exos:
                series = exostorage.load_series(exo_name)[0]
                if series is not None:
                    last_date = series.index[-1] + timedelta(days=1)
                    exec_time, decision_time = AssetIndexMongo.get_exec_time(last_date, self.asset_info)
                    self.logger.info('Updating existing {0} series from: {1}'.format(exo_name, decision_time))
                    exo_start_dates[exo_name] = decision_time

        else:
            self.logger.info('Updating new EXO series from: {0}'.format(self.args.backfill))
            exec_time, decision_time = AssetIndexMongo.get_exec_time(self.args.backfill, self.asset_info)

        exec_time_end, decision_time_end = AssetIndexMongo.get_exec_time(datetime.now(), self.asset_info)

        while current_time <= decision_time_end:
            self.logger.info("Backfilling: {0}".format(current_time))

            if self.check_bday_or_holiday(current_time):
                self.run_exo_calc(datasource, current_time, args.instrument, backfill_dict=exo_start_dates)

            current_time += timedelta(days=1)
            exec_time += timedelta(days=1)


    def main(self):
        self.logger.info("Initiating EXO building engine for {0}".format(self.args.instrument))

        # Initialize EXO engine SignalApp (report first status)
        self.signalapp = SignalApp(self.args.instrument, APPCLASS_EXO, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)
        self.signalapp.send(MsgStatus('INIT', 'Initiating EXO engine'))

        # Get information about decision and execution time
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        self.asset_info = assetindex.get_instrument_info(args.instrument)


        if self.args.backfill is not None:
            # Backfill mode enabled
            self.signalapp.send(MsgStatus("RUN",
                                          "Starting EXO backfill.".format(self.args.instrument),
                                          notify=True)
                                )
            self.do_backfill()
            self.signalapp.send(MsgStatus("RUN",
                                          "EXO backfill for {0} has been finished.".format(self.args.instrument),
                                          notify=True)
                                )
        else:
            # Online mode

            # Subscribe to datafeed signal app
            self.logger.debug('Subscribing datafeed for: ' + self.args.instrument)
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
        action="store",
        default='*')


    parser.add_argument(
        '-D',
        '--debug',
        help="Debug log files folder path if set",
        action="store",
        default=''
    )

    parser.add_argument(
        '-L',
        '--logfile',
        help="Log file for EXO builder script output",
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