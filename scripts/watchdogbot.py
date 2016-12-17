from slackclient import SlackClient
import time
import asyncio
from pymongo import MongoClient
from io import StringIO

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


class WatchdogBot:
    def __init__(self, channelid):
        self.client = SlackClient(SLACK_TOKEN)
        self.channelid = channelid

        status_client = MongoClient(MONGO_CONNSTR)
        self.status_db = status_client[MONGO_EXO_DB]

    def send_message(self, msg_text):
        self.client.api_call(
            "chat.postMessage",
            channel=self.channelid,
            text=msg_text
        )

    def command_status_quotes(self):
        with StringIO() as buff:
            buff.write("```Online quotes status:\n")
            buff.write(
                "{0:<20}{1:<15}{2:<25}{3:<25}{4:<25}\n".format('Instrument', 'Status', 'LastBarInDB', 'LastRunTime',
                                                               'Now'))
            for data in self.status_db[STATUS_QUOTES_COLLECTION].find():
                buff.write(
                    "{0:<20}{1:<15}{2!s:<25}{3!s:<25}{4!s:<25}\n".format(data['instrument'],
                                                                   data['quote_status'],
                                                                   data['last_bar_time'],
                                                                   data['last_run_date'],
                                                                   data['now']))
            buff.write("```")
            self.send_message(buff.getvalue())

    def command_help(self):
        self.send_message("""Watchdog Bot help, commands usage:
        `help` - displays this message

        *Status information:*
        `status` - brief status of the system
        `status quotes` - quotes status per product
        """)

    def command_default(self):
        self.send_message("Type `help` to get commands description")

    def process_message(self, msg_data):
        msg = msg_data['text'].lower().strip()
        channel = msg_data['channel']

        if channel != self.channelid:
            return

        if msg == 'help':
            self.command_help()
        elif msg == 'status quotes':
            self.command_status_quotes()
        else:
            self.command_default()

    @asyncio.coroutine
    def run_bot(self):
        if self.client.rtm_connect():
            while True:
                data = self.client.rtm_read()
                if len(data) > 0:
                    for d in data:
                        if d['type'] == 'message':
                            if 'subtype' not in d or d['subtype'] != 'bot_message':
                                self.process_message(d)
                    print(data)
                time.sleep(1)
        else:
            print("Connection Failed, invalid token?")

if __name__ == '__main__':
    wd = WatchdogBot(SLACK_CHANNEL)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wd.run_bot())
