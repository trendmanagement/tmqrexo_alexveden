from exobuilder.exo.position import Position
from exobuilder.exo.transaction import Transaction
import pandas as pd
import pickle
import os
import datetime
import warnings


class ExoEngineBase(object):
    """
    List of products for current EXO calculation.
    If None the exo will be calculated for each asset
    If list like ['CL', 'ES', 'ZW'] - only defined assets will be calculated
    """
    ASSET_LIST = None


    def __init__(self, symbol, direction, date, datasource, **kwargs):
        self._position = Position()
        self._date = date
        self._datasource = datasource
        self._series = pd.DataFrame()
        self._extra_context = {}
        self._transactions = []
        self._old_transactions = []
        log_file_path = kwargs.get('log_file_path', '')
        is_eod = kwargs.get('is_eod', True)

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

    def get_custom_values(self):
        """
        Method that return custom EXO data frame values, to store inside EXO Dataframe in the DB
        :return: dictionary {'string_key': (int or float) value}
        """
        return {}

    def calculate(self):
        """
        Main internal method to manage EXO data
        :return:
        """
        trans_list = []
        roll_trans = []

        # Proto-code
        is_rollover = self.is_rollover()
        if is_rollover:
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

        # Setting EXO data and delta to EXO dataframe
        self.series.at[dt, 'exo'] = pnl
        self.series.at[dt, 'delta'] = self.position.delta
        self.series.at[dt, 'is_rollover'] = 1 if is_rollover else 0

        # Store number of contracts traded
        nfutures_executed = 0
        nfutures_opened = 0
        noptions_executed = 0
        noptions_opened = 0

        for t in trans_list:
            if t.asset.contract_type == 'opt':
                noptions_executed += abs(t.qty)  # <-- to avoid long/short netting

            if t.asset.contract_type == 'fut':
                nfutures_executed += abs(t.qty)  # <-- to avoid long/short netting

        for asset, pos in self.position.netpositions.items():
            if asset.contract_type == 'opt':
                noptions_opened += abs(pos['qty'])  # <-- to avoid long/short netting
            if asset.contract_type == 'fut':
                nfutures_opened += abs(pos['qty'])  # <-- to avoid long/short netting

        self.series.at[dt, 'nfutures_executed'] = nfutures_executed
        self.series.at[dt, 'nfutures_opened'] = nfutures_opened

        self.series.at[dt, 'noptions_executed'] = noptions_executed
        self.series.at[dt, 'noptions_opened'] = noptions_opened

        for k,v in self.get_custom_values().items():
            if not isinstance(k, str):
                raise ValueError("Key of custom_exo_values must be string")
            if not isinstance(v, (int, float,)):
                raise ValueError("Value of custom_exo_values must be int or float")

            self.series.at[dt, k] = v

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

        result['calc_date'] = datetime.datetime.now()

        return result

    @staticmethod
    def check_series_integrity(exo_name, exo_df, raise_exception=False):
        if len(exo_df) < 200:
            if raise_exception:
                raise ValueError("{0} [NODATA DataLen: {1}]".format(exo_name, len(exo_df)))
            else:
                warnings.warn("{0} [NODATA DataLen: {1}]".format(exo_name, len(exo_df)))
                return False
        elif (datetime.datetime.now() - exo_df.index[-1]).days > 4:
            if raise_exception:
                raise ValueError("{0} [DELAYED: LastDate: {1}]".format(exo_name, exo_df.index[-1]))
            else:
                warnings.warn("{0} [DELAYED: LastDate: {1}]".format(exo_name, exo_df.index[-1]))
                return False
        else:
            return True

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

    def log(self, message):
        if self.logger is not None:
            self.logger.write(message + '\n')

    def _log_transactions(self, trans_list):
        if self.logger is not None:
            for t in trans_list:
                self.logger.write("Transaction:\t {0}\n".format(t))

    def __str__(self):
        return self.exo_name

