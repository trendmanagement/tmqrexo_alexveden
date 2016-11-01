from exobuilder.exo.position import Position
from exobuilder.exo.transaction import Transaction
import pandas as pd
import pickle
import os
import datetime


class ExoEngineBase(object):
    def __init__(self, symbol, direction, date, datasource, log_file_path='', is_eod=True):
        self._position = Position()
        self._date = date
        self._datasource = datasource
        self._series = pd.DataFrame()
        self._extra_context = {}
        self._transactions = []
        self._old_transactions = []
        self.debug_mode = log_file_path != ''
        self.logger = None
        self.is_eod = is_eod

        if self.debug_mode:
            if not os.path.exists(log_file_path):
                raise ValueError("log_file_path doesn't exists")

            self.logger = open(os.path.join(log_file_path, self.name+'.log'), 'a')
            self.logger.write("\nProcessing {0}\n".format(date))

    @staticmethod
    def names_list(symbol):
        raise NotImplementedError("Each EXO class must implement names_list")

    @staticmethod
    def direction_type():
        raise NotImplementedError("Each EXO class must implement direction type 1 Long, -1 Short, 0 Bidirectional")

    @property
    def name(self):
        return self.exo_name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        if self.logger is not None:
            self.logger.close()
            self.logger = None

    @property
    def exo_name(self):
        raise NotImplementedError("This method must be overridden by child class of EXO engine")

    def is_rollover(self):
        raise NotImplementedError("This method must be overridden by child class of EXO engine")

    def process_rollover(self):
        """
        Typically we should only close old position on rollover day
        :return:
        """
        raise NotImplementedError("This method must be overridden by child class of EXO engine")

    def process_day(self):
        """
        Main EXO's position management method
        :return: list of Transactions to process
        """
        raise NotImplementedError("This method must be overridden by child class of EXO engine")

    def calculate(self, custom_exo_values={}):
        """
        Main internal method to manage EXO data
        :return:
        """
        trans_list = []
        roll_trans = []

        # Proto-code
        if self.is_rollover():
            if self.debug_mode:
                self.logger.write("Rollover event occured\n")

            roll_trans = self.process_rollover()
            if roll_trans is not None and len(roll_trans) > 0:
                trans_list += roll_trans
                if self.debug_mode:
                    self.logger.write("Rolling position\n")
                    self._log_transactions(roll_trans)

                for t in roll_trans:
                    self.position.add(t)

            # Process closed position PnL to change EXO price for current day
            # ???

        # Processing new day
        new_transactions = self.process_day()
        if new_transactions is not None and len(new_transactions) > 0:

            if self.debug_mode:
                self.logger.write("OLD position:\n")
                self.logger.write(str(self.position)+'\n')
                self._log_transactions(new_transactions)

            trans_list += new_transactions
            for t in new_transactions:
                self.position.add(t)

            if self.debug_mode:
                self.logger.write("NEW position:\n")
                self.logger.write(str(self.position) + '\n')
        else:
            if self.debug_mode:
                self.logger.write("Current position:\n")
                self.logger.write(str(self.position) + '\n')


        self._transactions += trans_list

        pnl = self.position.pnl

        if self.is_eod:
            dt = datetime.datetime.combine(self.date.date(), datetime.time(0, 00))
        else:
            dt = self.date
        self.series.at[dt, 'exo'] = pnl

        if self.is_eod:
            dt = datetime.datetime.combine(self.date.date(), datetime.time(0, 00))
            self.series.at[dt, 'exo'] = pnl
        else:
            self.series.at[self.date, 'exo'] = pnl

        for k,v in custom_exo_values.items():
            if not isinstance(k, str):
                raise ValueError("Key of custom_exo_values must be string")
            if not isinstance(v, (int, float,)):
                raise ValueError("Value of custom_exo_values must be int or float")

            self.series[dt, k] = v

        # Save EXO state to DB
        self.save()







    def as_dict(self):
        """
        Save the EXO data to DB
        :return:
        """
        result = {}

        result['position'] = self.position.as_dict()

        result['transactions'] = self._old_transactions

        for t in self._transactions:
            result['transactions'].append(t.as_dict())

        result['name'] = self.name

        result['series'] = pickle.dumps(self.series)

        return result

    def load(self):
        exo_data = self.datasource.exostorage.load_exo(self.name)
        if exo_data is not None:
            self._position = Position.from_dict(exo_data['position'], self.datasource, self.date)
            self._old_transactions = exo_data['transactions']
            self._series = pickle.loads(exo_data['series'])
        return exo_data

    def save(self):
        """
        Save EXO data to storage
        :return:
        """
        self.datasource.exostorage.save_exo(self.as_dict())


    @property
    def position(self):
        """
        Returns current opened position of EXO engine
        If position is closed return None
        :return: None or Position()
        """
        return self._position

    @property
    def series(self):
        """
        Returns EXO price series values (before current date)
        :return:
        """
        return self._series

    @property
    def date(self):
        return self._date

    @property
    def datasource(self):
        return self._datasource

    def _log_transactions(self, trans_list):
        for t in trans_list:
            self.logger.write("Transaction:\t {0}\n".format(t))