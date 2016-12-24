from slackclient import SlackClient
import time
from pymongo import MongoClient
from io import StringIO
from tradingcore.signalapp import SignalApp
from tradingcore.messages import *
from concurrent.futures import  ThreadPoolExecutor, thread
from collections import OrderedDict
import sys
import logging
import subprocess
import re
import bdateutil
import holidays
from scripts.event_logger import EVENTS_STATUS, EVENTS_LOG

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
        logger = logging.getLogger('WatchdogBot')
        logger.setLevel(logging.INFO)

        # create console handler with a higher log level
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        self.log = logger

        self.client = None
        self.channelid = channelid

        status_client = MongoClient(MONGO_CONNSTR)
        self.status_db = status_client[MONGO_EXO_DB]

        self.antiflood_status = {}
        self.antiflood_delay_minutes = 30

    def check_antiflood(self, appclass, appname, status_msg, dtnow):
        key = "{0}.{1}".format(appclass, appname)

        if key not in self.antiflood_status:
            self.antiflood_status[key] = {'status': status_msg.status, 'last_message': dtnow}
            return True
        else:
            afld = self.antiflood_status[key]
            if afld['status'] != status_msg.status:
                afld['status'] = status_msg.status
                return True
            if (dtnow-afld['last_message']).total_seconds()/60 > self.antiflood_delay_minutes:
                afld['last_message'] = dtnow
                return True

        self.log.debug('Skipping antiflood message')
        return False



    def send_notification(self, appname, appclass, msg):
        """
        Pushing RabbitMQ notifications to Slack with flood control
        :param appname:
        :param appclass:
        :param msg:
        :return:
        """
        if self.check_antiflood(appclass, appname, msg, datetime.now()):
            self.send_message("{0}.{1}: [{2}] {3}".format(appclass, appname, msg.status,  msg.message))

    def send_message(self, msg_text, attachments=None):
        if self.client is not None:
            if attachments is None:
                self.client.api_call(
                    "chat.postMessage",
                    channel=self.channelid,
                    text=msg_text
                )
            else:
                self.client.api_call(
                    "chat.postMessage",
                    channel=self.channelid,
                    text=msg_text,
                    attachments=attachments
                )
        else:
            logging.info("Trying to send message to null client: {0}".format(msg_text))

    def get_shell_command_output(self, cmd_args):
        """
        Run OS command and return its output
        :param cmd_args:
        :return: text output or None if command exit code != 0
        """
        try:
            return subprocess.check_output(cmd_args).decode()
        except subprocess.CalledProcessError as exc:
            self.log.error("Failed to run command {0} output:\n {1}".format(cmd_args, exc.output))
            return None

    def check_supervisor_apps(self):
        """
        Process 'supervisorctl status' output and get statistict
        :return:
        """
        output = self.get_shell_command_output(['supervisorctl', 'status'])
        if output is None:
            return 'N/A'
        else:
            if len(output) == 0:
                return 'N/A'
            statuses = OrderedDict()

            for line in output.splitlines():
                l = line.strip()
                if len(l) == 0:
                    continue

                toks = re.sub(r'\s+', ' ', line).split()

                if len(toks) < 2:
                    continue
                status = toks[1]

                statuses.setdefault(status, 0)
                statuses[status] += 1

            with StringIO() as buff:
                for k,v in statuses.items():
                    buff.write("{0}:{1} ".format(k, v))
                return buff.getvalue()

    def check_current_scripts_status(self):
        statuses = OrderedDict()
        for status_rec in self.status_db[EVENTS_STATUS].find({}):
            status = status_rec['status']
            statuses.setdefault(status, 0)
            statuses[status] += 1

        with StringIO() as buff:
            for k, v in statuses.items():
                buff.write("{0}:{1} ".format(k, v))
            return buff.getvalue()



    def command_status(self):
        with StringIO() as buff:
            buff.write("System status summary:\n")
            buff.write("```")
            buff.write("Supervisor scripts status: {0}\n".format(self.check_supervisor_apps()))
            buff.write("Apps status: {0}\n".format(self.check_current_scripts_status()))
            buff.write("```")
            self.send_message(buff.getvalue())



    def command_status_supervisor(self):
        output = self.get_shell_command_output(['supervisorctl', 'status'])
        if output is None:
            self.send_message("`supervisorctl status` execution failed, look into log for more information")
        else:
            with StringIO() as buff:
                buff.write("Online applications status:\n")
                buff.write("```")
                buff.write(output)
                buff.write("```")
                self.send_message(buff.getvalue())



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
        `status` - System status summary
        `status quotes` - Quotes status per product
        `status apps` - Last internal status of scripts
        `status supervisor` - Status of running applications inside Supervisor daemon

        *Events log information:*
        `events log <count>` - returns <count> records of last occurred events
        """)

    def command_default(self):
        self.send_message("Type `help` to get commands description")

    def command_status_apps(self):

        with StringIO() as buff:
            buff.write("Last status:\n")
            buff.write("```")
            for status_rec in self.status_db[EVENTS_STATUS].find({}).sort([("appclass", 1), ("appname", 1)]):
                status = status_rec['status']
                msg = status_rec['text']

                buff.write("{0:<15}{1:<30}{2:>10}   {3}\n".format(
                    status_rec['date'].strftime('%d-%b %H:%M'),
                    status_rec['appclass'] + '.' + status_rec['appname'],
                    status,
                    msg
                ))
            buff.write("```")
            return self.send_message(buff.getvalue())

    def command_events_log(self, msg):
        try:
            count = int(msg.split()[2])
        except:
            return self.send_message("Bad syntax, try to type `events log 20`")

        with StringIO() as buff:
            buff.write("Last events:\n")
            buff.write("```")
            for status_rec in self.status_db[EVENTS_LOG].find({}).sort([("date", -1)]).limit(count):
                msg = status_rec['text']

                buff.write("{0:<15}{1:<50}{2:>15}   {3}\n".format(
                    status_rec['date'].strftime('%d-%b %H:%M'),
                    status_rec['appclass'] + '.' + status_rec['appname'],
                    status_rec['msgtype'],
                    msg
                ))
            buff.write("```")
            return self.send_message(buff.getvalue())


    def process_message(self, msg_data):
        msg = msg_data['text'].lower().strip()
        channel = msg_data['channel']

        if channel != self.channelid:
            return

        if msg == 'help':
            self.command_help()
        elif msg == 'status':
            self.command_status()
        elif msg == 'status quotes':
            self.command_status_quotes()
        elif msg == 'status apps':
            self.command_status_apps()
        elif msg == 'status supervisor':
            self.command_status_supervisor()
        elif 'events log' in msg:
            self.command_events_log(msg)
        else:
            self.command_default()

    def listen_apps(self):
        # Waiting slack bot to connect first
        time.sleep(2)
        self.log.info("Listening for events")

        def callback(appclass, appname, msg):
            try:
                if msg.mtype == MsgStatus.mtype:
                    if msg.notify:
                        self.log.info("Notification: {0}.{1}: {2}".format(appclass, appname, msg))
                        self.send_notification(appname, appclass, msg)
                    self.log.info("Incoming status: {0}.{1}: {2}".format(appclass, appname, msg))
            except Exception:
                self.log.error("Failed to process: {0}.{1}: {2}".format(appclass, appname, msg))
                self.log.exception('Error while processing message')

        try:
            app = SignalApp('*', '*')
            app.listen(callback)
        except Exception:
            self.log.exception('Error while listening RabbitMQ')
            self.send_message("Exception occurred while processing framework messages, look into logs for information")

    def run_bot(self):
        self.log.info("Launching bot")
        self.client = SlackClient(SLACK_TOKEN)
        if not self.client.rtm_connect():
            self.log.error("Connection Failed, invalid token?")
        else:
            self.log.info("Slack engine connected")

        while True:
            data = self.client.rtm_read()
            if len(data) > 0:
                for d in data:
                    if d['type'] == 'message':
                        if 'subtype' not in d or d['subtype'] != 'bot_message':
                            try:
                                self.process_message(d)
                                self.log.info('Incoming message: {0}'.format(data))
                            except:
                                self.log.exception("Error while processing message")
            time.sleep(1)


if __name__ == '__main__':
    wd = WatchdogBot(SLACK_CHANNEL)

    with ThreadPoolExecutor(max_workers=4) as e:
        try:
            e.submit(wd.run_bot)
            e.submit(wd.listen_apps)
        except KeyboardInterrupt:
            e.shutdown(wait=False)
            e._threads.clear()
            thread._threads_queues.clear()
            raise

