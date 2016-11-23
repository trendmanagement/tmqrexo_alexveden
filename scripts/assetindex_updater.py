"""
Scheduled asset index updater

Loads information about assets metadata from SQL server and save it to MongoDB.

Loads information about recently added:

* Instruments
* Futures
* Options
"""
# import modules used here -- sys is a very standard one
import sys, argparse, logging
import pymssql
import _mssql
import datetime
from decimal import Decimal
import pymongo
from pymongo import MongoClient


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

#
# Handling unexpected exceptions
#
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception


def convert_dates(values):
    k,v = values
    if type(v) == datetime.date:
        return k, datetime.datetime.combine(
                v,
                datetime.datetime.min.time())
    if type(v) == Decimal:
        return k, float(v)
    else:
        return k, v

def get_sql_data(sql_conn, mongo_db, colname):
    logging.info("Processing: " + colname)
    lastid = -1
    idname = ''
    if colname == 'options':
        idname = 'idoption'
        last_data = mongo_db[colname].find({}).sort(idname, pymongo.DESCENDING).limit(1).next()
        lastid = last_data[idname]
        logging.info('Updating Options from ID:{0}'.format(lastid))
    elif colname == 'contracts':
        idname = 'idcontract'
        last_data = mongo_db[colname].find({}).sort(idname, pymongo.DESCENDING).limit(1).next()
        lastid = last_data[idname]
        logging.info('Updating Futures from ID:{0}'.format(lastid))
    elif colname == 'instruments':
        idname = 'idinstrument'
        last_data = mongo_db[colname].find({}).sort(idname, pymongo.DESCENDING).limit(1).next()
        lastid = last_data[idname]
        logging.info('Updating Instruments from ID:{0}'.format(lastid))

    qry = 'SELECT * FROM cqgdb.tbl{0} WHERE {1} > {2}'.format(colname, idname, lastid)
    logging.debug(qry)
    c2 = sql_conn.cursor(as_dict=True)
    c2.execute(qry)
    collection = mongo_db[colname]

    cnt = 0
    for row in c2:
        try:
            data = dict(map(convert_dates, row.items()))
            collection.insert_one(data)
            cnt += 1
        except TypeError:
            logging.error("TypeError: {0}".format(row))
            logging.error("Stop processing")
            break

    logging.debug('{0} - {1} rows prosessed'.format(colname, cnt))

# Gather our code in a main() function
def main(args, loglevel):
    logging.getLogger("pika").setLevel(logging.WARNING)

    if args.logfile == '':
        logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=loglevel)
    else:
        logging.basicConfig(filename=args.logfile, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=loglevel)
    logging.info('Starting...')

    logging.debug("Connecting to Mongo DB: " + MONGO_CONNSTR)
    client = MongoClient(MONGO_CONNSTR)
    mongo_db = client[MONGO_EXO_DB]

    logging.info("Connecting to SQL Server DB {0}  {1}".format(SQL_HOST, 'TMLDB'))
    sql_conn = pymssql.connect(SQL_HOST, SQL_USER + "@" + SQL_HOST, SQL_PASS, 'TMLDB')

    logging.info("Requesting information...")



    get_sql_data(sql_conn, mongo_db, 'instruments')

    get_sql_data(sql_conn, mongo_db, 'contracts')

    get_sql_data(sql_conn, mongo_db, 'options')



    sql_conn.close()
    client.close()
    logging.info('Done.')



# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Data uploading script for asset index creation. TML SQL Azure DB to local MongoDB",
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

    main(args, loglevel)