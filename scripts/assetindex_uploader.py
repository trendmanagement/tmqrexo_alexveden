#!/usr/bin/env python
#

# import modules used here -- sys is a very standard one
import sys, argparse, logging
import pymssql
import _mssql
import datetime
from decimal import Decimal
import pymongo
from pymongo import MongoClient

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
    qry = 'SELECT * FROM cqgdb.tbl' + colname
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

    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    logging.debug("Connecting to Mongo DB: " + args.mongodb)
    client = MongoClient(args.mongodb)
    mongo_db = client['tmldb']

    logging.info("Connecting to SQL Server DB {0}  {1}".format(args.sqlserver, args.sqldb))
    sql_conn = pymssql.connect(args.sqlserver, args.sqluser + "@" + args.sqlserver, args.sqlpassword, args.sqldb)

    logging.info("Requesting information...")

    get_sql_data(sql_conn, mongo_db, 'instruments')

    get_sql_data(sql_conn, mongo_db, 'contracts')

    get_sql_data(sql_conn, mongo_db, 'options')

    sql_conn.close()
    client.close()





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
        "-m",
        "--mongodb",
        help="Connection string for MongoDB default: %(default)s",
        action="store",
        default='mongodb://localhost:27017/')

    parser.add_argument(
        "-S",
        "--sqlserver",
        help="SQL server address default: %(default)s",
        action="store",
        default='h9ggwlagd1.database.windows.net')

    parser.add_argument(
        "-U",
        "--sqluser",
        help="SQL server user name default: %(default)s",
        action="store",
        default='modelread')

    parser.add_argument(
        "-P",
        "--sqlpassword",
        help="SQL server password default: %(default)s",
        action="store",
        default='4fSHRXwd4u')

    parser.add_argument(
        "-D",
        "--sqldb",
        help="SQL server database name default: %(default)s",
        action="store",
        default='TMLDB')




    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)