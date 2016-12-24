"""
Online alpha execution script for custom alphas (calculated for only particular EXO)

"""

# import modules used here -- sys is a very standard one
import logging
import sys

from tradingcore.signalapp import SignalApp

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

from tradingcore.messages import *
import pymongo
from pymongo import MongoClient

EVENTS_STATUS = 'events_status'
EVENTS_LOG = 'events_log'


class EventLoggerScript:
    def __init__(self):
        loglevel = logging.DEBUG
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

        self.log.info('Init Event logger script')
        self.signal_app = SignalApp('*', '*', RABBIT_HOST, RABBIT_USER, RABBIT_PASSW)

        client = MongoClient(MONGO_CONNSTR)
        self.db = client[MONGO_EXO_DB]
        self.prepare_db()

    def prepare_db(self):
        self.db[EVENTS_STATUS].create_index([('appclass', pymongo.ASCENDING), ('appname', pymongo.ASCENDING)], background=True)
        self.db[EVENTS_LOG].create_index([('date', pymongo.DESCENDING)], background=True)

    def log_event(self, appclass, appname, date, msgtype, msgtext):
        msg_dict = {
            'appclass': appclass,
            'appname': appname,
            'msgtype': msgtype,
            'date': date,
            'text': msgtext,
        }
        self.db[EVENTS_LOG].insert_one(msg_dict)

    def process_message_status(self, appclass, appname, msg):
        msg_dict = {
            'appclass': appclass,
            'appname': appname,
            'status': msg.status,
            'date': msg.date,
            'text': msg.message,
        }
        self.db[EVENTS_STATUS].replace_one({'appclass': appclass, 'appname': appname}, msg_dict, upsert=True)
        self.log_event(appclass, appname, msg.date, msg.mtype, '{0}: {1}'.format(msg.status, msg.message))

    def process_message_quotenotification(self, appclass, appname, msg):
        msg_text = 'Quote: {0} at {1}'.format(msg.instrument, msg.date)
        self.log_event(appclass, appname, datetime.now(), msg.mtype, msg_text)

    def process_message_exoquote(self, appclass, appname, msg):
        msg_text = 'EXOQuote: {0} at {1}'.format(msg.exo_name, msg.exo_date)
        self.log_event(appclass, appname, datetime.now(), msg.mtype, msg_text)

    def process_message_alphasignal(self, appclass, appname, msg):
        msg_text = 'AlphaSignal: {0} Exposure {1} AccountsCount: {2}'.format(msg.swarm_name, msg.exposure, len(msg.positions))
        self.log_event(appclass, appname, datetime.now(), msg.mtype, msg_text)

    def process_message_alphastate(self, appclass, appname, msg):
        msg_text = 'AlphaState: {0} Exposure {1} LastDate: {2}'.format(msg.swarm_name, msg.exposure, msg.last_date)
        self.log_event(appclass, appname, datetime.now(), msg.mtype, msg_text)

    def process_event_callback(self, appclass, appname, msg):
        self.log.info("New message {0}.{1}: {2}".format(appclass, appname, msg))

        if msg.mtype == MsgStatus.mtype:
            self.process_message_status(appclass, appname, msg)
        elif msg.mtype == MsgQuoteNotification.mtype:
            self.process_message_quotenotification(appclass, appname, msg)
        elif msg.mtype == MsgEXOQuote.mtype:
            self.process_message_exoquote(appclass, appname, msg)
        elif msg.mtype == MsgAlphaSignal.mtype:
            self.process_message_alphasignal(appclass, appname, msg)
        elif msg.mtype == MsgAlphaState.mtype:
            self.process_message_alphastate(appclass, appname, msg)



    def main(self):
        """
        Application main()
        :return:
        """
        # Subscribe to rabbit MQ EXO feed
        self.signal_app.listen(self.process_event_callback)



# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    script = EventLoggerScript()
    script.main()



