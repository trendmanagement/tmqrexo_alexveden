"""
Scheduled script for account positions archiving


"""
# import modules used here -- sys is a very standard one
import sys, argparse, logging
from tradingcore.signalapp import SignalApp, APPCLASS_UTILS
from pymongo import MongoClient
from pymongo import ReplaceOne
from pymongo.errors import BulkWriteError

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
import datetime
import holidays
import bdateutil

class TradingPositionsArchiveScript:
    def __init__(self, args, loglevel):
        self.args = args
        self.loglevel = loglevel
        logging.getLogger("pika").setLevel(logging.WARNING)
        logger = logging.getLogger('TradingPositionsArchiveScript')
        logger.setLevel(loglevel)

        fh = None
        if args.logfile != '':
            fh = logging.FileHandler(args.logfile)
            fh.setLevel(loglevel)

        # create console handler with a higher log level
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(loglevel)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        if fh is not None:
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        self.log = logger

        self.log.info('Init TradingPositionsArchive')

        self.signal_app = SignalApp('TradingPositionsArchive', APPCLASS_UTILS, RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)
        self.signal_app.send(MsgStatus("INIT", 'Initiating TradingPositionsArchive'))

        self.mongo_client = MongoClient(MONGO_CONNSTR)
        self.mongo_db = self.mongo_client[MONGO_EXO_DB]

    def run(self):
        """
        Application main()
        :return:
        """
        if not bdateutil.isbday(datetime.datetime.now(), holidays=holidays.US()):
            self.log.info("Run is skipped due to non business day")
            self.signal_app.send(MsgStatus("SKIPPED",
                                           "Run is skipped due to non business day",
                                           notify=False,
                                           )
                                 )
            return

        # Populating account positions
        operations = []
        update_date = 'N/A'

        for acc_pos_dict in self.mongo_db['accounts_positions'].find({}):
            # Shrinking time of the timestamp
            update_date = datetime.datetime.combine(acc_pos_dict['date_now'].date(), datetime.time(0,0,0))
            # 'date_now' - main timestamp of collection
            acc_pos_dict['date_now'] = update_date

            del acc_pos_dict['_id']

            # Add MongoDB bulk operation
            operations.append(ReplaceOne(
                {'date_now': update_date, 'name': acc_pos_dict['name']},
                acc_pos_dict,
                upsert=True,
            ))
        self.log.info("Last collection update date: {0}".format(update_date))
        # Execute bulk upsert to Mongo
        pp = pprint.PrettyPrinter(indent=4)
        try:
            bulk_result = self.mongo_db['accounts_positions_archive'].bulk_write(operations, ordered=False)
            self.log.info("Bulk write result succeed: \n{0}".format(pp.pformat(bulk_result.bulk_api_result)))

            self.signal_app.send(MsgStatus("OK",
                                           "Positions archive created",
                                           notify=True,
                                           )
                                 )
        except BulkWriteError as exc:
            self.log.error("Bulk write error occured: {0}".format(pp.pformat(exc.details)))
            self.signal_app.send(MsgStatus("ERROR",
                                           "Positions archive error while writing to MongoDB",
                                           notify=True,
                                           )
                                 )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Trading orders archive script",
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

    script = TradingPositionsArchiveScript(args, loglevel)
    script.run()