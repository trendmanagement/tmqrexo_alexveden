import importlib
import logging
import time
from datetime import datetime, timedelta, time as dttime

from pymongo import MongoClient

from exobuilder.algorithms.rollover_helper import RolloverHelper
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.exostorage import EXOStorage
import matplotlib.pyplot as plt
importlib.reload(logging);
import warnings

from backtester.reports.payoffs import PayoffAnalyzer

from scripts.settings import *
from scripts.tmqrholidays import TMQRHolidays
import bdateutil
import holidays


#try:
#    from scripts.settings_local import *
#except ImportError:
#    pass



class SmartEXOUtils:
    def __init__(self, smartexo_class, **kwargs):
        self.verbosive_logging = kwargs.get('verbosive_logging', False)
        self.futures_limit = kwargs.get('futures_limit', 3)
        self.options_limit = kwargs.get('options_limit', 20)
        self.smartexo_class = smartexo_class

        if self.verbosive_logging:
            logging.basicConfig(format='%(message)s', level=logging.DEBUG)
        else:
            logging.basicConfig(format='%(message)s', level=logging.INFO)

        self.assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        self.exostorage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

        #self.datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, self.assetindex,
        #                                self.futures_limit, self.options_limit,
        #                                self.exostorage)
        self.datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, self.assetindex,
                                          self.futures_limit, self.options_limit,
                                          self.exostorage)

    def plot_transactions_payoff(self, smart_exo_position_func, analysis_date, analysis_instrument, **whatif_kwargs):

        payoff = PayoffAnalyzer(self.datasource)
        instr = self.datasource.get(analysis_instrument, analysis_date)
        rh = RolloverHelper(instr)
        fut, opt_chain = rh.get_active_chains()

        strikes_on_graph = whatif_kwargs.get('strikes_on_graph', 30)
        whatif_iv_change = whatif_kwargs.get('whatif_iv_change', 0)
        whatif_days_to_expiration = whatif_kwargs.get('whatif_days_to_expiration', int(opt_chain.to_expiration_days / 2))

        payoff.load_transactions(smart_exo_position_func(analysis_date, fut, opt_chain), analysis_date)
        payoff.plot(strikes_on_graph, whatif_iv_change, whatif_days_to_expiration)

    def clear_smartexo(self):
        logging.info("Deleting all SmartEXO of :" + self.smartexo_class.EXO_NAME)
        client = MongoClient(MONGO_CONNSTR)
        db = client[MONGO_EXO_DB]
        db['exo_data'].delete_many({'name': {'$regex': '.*{0}*.'.format(self.smartexo_class.EXO_NAME)}})

    def build_smartexo(self, start_date, **smartexo_kwargs):
        def check_bday_or_holiday(date):
            if date.weekday() >= 5 or not bdateutil.isbday(date, holidays=TMQRHolidays()):
                # Skipping weekends and US holidays
                # date.weekday() >= 5 - 5 is Saturday!
                return False

            return True
        self.clear_smartexo()

        logging.info("Starting EXO calculation process from: {0}".format(start_date))

        if self.smartexo_class.ASSET_LIST is None:
            warnings.warn("You must define ASSET_LIST inside SmartEXO class. Aborting...")
            return

        for ticker in self.smartexo_class.ASSET_LIST:
            logging.info("Processing: " + ticker)
            currdate = start_date
            enddate = datetime.combine(datetime.now().date(), dttime(0, 0, 0))

            while currdate <= enddate:
                start_time = time.time()
                date = currdate

                asset_info = self.assetindex.get_instrument_info(ticker)
                exec_time_end, decision_time_end = AssetIndexMongo.get_exec_time(date, asset_info)

                if check_bday_or_holiday(decision_time_end):
                    logging.debug("\t\tRun on {0}".format(decision_time_end))
                    with self.smartexo_class(ticker, 0, decision_time_end, self.datasource, **smartexo_kwargs) as exo_engine:
                        try:
                            asset_list = exo_engine.ASSET_LIST
                            # Checking if current symbol is present in EXO class ASSET_LIST
                            if asset_list is not None:
                                if ticker not in asset_list:
                                    # Skipping assets which are not in the list
                                    continue
                        except AttributeError:
                            warnings.warn(
                                "EXO class {0} doesn't contain ASSET_LIST attribute filter, calculating all assets".format(self.smartexo_class))
                        try:
                            # Load EXO information from mongo
                            exo_engine.load()
                            exo_engine.calculate()
                        except Exception as exc:
                            logging.error("ERROR!: {0}".format(exc))

                end_time = time.time()
                currdate += timedelta(days=1)
                logging.debug("Elapsed: {0}".format(end_time - start_time))
        logging.info('Done')

    def plot_smartexo_price(self):
        if self.smartexo_class.ASSET_LIST is None:
            warnings.warn("You must define ASSET_LIST inside SmartEXO class. Aborting...")
            return

        for ticker in self.smartexo_class.ASSET_LIST:
            exo_df, exo_info = self.exostorage.load_series('{0}_{1}'.format(ticker, self.smartexo_class.EXO_NAME))

            f, (ax1, ax2) = plt.subplots(2, gridspec_kw={'height_ratios': [3, 1]})

            exo_df['exo'].plot(ax=ax1, title='{0}_{1}'.format(ticker, self.smartexo_class.EXO_NAME))

            if 'regime' in exo_df:
                ax = exo_df['regime'].plot(ax=ax1, secondary_y=True)
                ax.set_ylim(-2, 2)

            exo_df['delta'].plot(ax=ax2);
            ax2.set_title('Delta');
            plt.show();
