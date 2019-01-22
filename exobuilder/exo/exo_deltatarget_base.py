import importlib
import logging
import sys

importlib.reload(logging);

from exobuilder.exo.exoenginebase import ExoEngineBase
from exobuilder.algorithms.rollover_helper import RolloverHelper


def ipython_info():
    ip = False
    if 'ipykernel' in sys.modules:
        ip = 'notebook'
    elif 'IPython' in sys.modules:
        ip = 'terminal'
    return ip


class EXODeltaTargetBase(ExoEngineBase):
    EXO_NAME = "EXODeltaTargetBase"

    def __init__(self, symbol, direction, date, datasource, log_file_path=''):
        self._direction = direction
        self._symbol = symbol

        if ipython_info():
            self.console_logging = True
            logging.basicConfig(format='%(message)s', level=logging.DEBUG)
        else:
            self.console_logging = False

        super().__init__(symbol, direction, date, datasource, log_file_path=log_file_path)

    @staticmethod
    def direction_type():
        # Fixed at 2017-03-14 (return value was 0)
        # SmartEXOs has unified direction, direction = 0 lead to double SmartEXO calculation in smart exo script
        # Returning 1 we are sure that SmartEXO calculates only once
        return 1

    @classmethod
    def names_list(cls, symbol):
        return ['{0}_{1}'.format(symbol, cls.EXO_NAME)]

    @property
    def exo_name(self):
        return '{0}_{1}'.format(self._symbol, self.EXO_NAME)

    def is_rollover(self):
        if len(self.position) != 0:
            for asset, netposition in self.position.netpositions.items():
                rh = RolloverHelper(asset.instrument)
                if rh.is_rollover(asset):
                    return True
        return False

    def process_rollover(self):
        trans_list = self.position.close_all_translist()
        self.log('{0}: Rollover occured, new series used'.format(self.date))
        return trans_list

    @staticmethod
    def new_position(date, fut, opt_chain):
        """
        Returns transaction to open new EXO position
        params date: current date
        params fut: current actual future contract
        params opt_chain: current actual options chain

        returns: List of Transactions to open
        """
        return []

    def is_position_needs_rebalance(self, opened_position):
        """
        Checks if opened position meets conditions when it should be closed and reopened
        """
        return False

    def process_day(self):
        """
        Main EXO's position management method
        :return: list of Transactions to process
        """
        trans_list = []
        instr = self.datasource.get(self._symbol, self.date)
        rh = RolloverHelper(instr)
        fut, opt_chain = rh.get_active_chains()
        if fut is None or opt_chain is None:
            raise ValueError("Active option chain is not found for {0}".format(self._symbol))

        if len(self.position) == 0:
            self.log("{0}: Position is empty, executing new position".format(self.date))
            return self.new_position(self.date, fut, opt_chain)
        elif self.is_position_needs_rebalance(self.position):
            self.log("{0}: Position needs rebalance".format(self.date))
            trans_list += self.position.close_all_translist()
            trans_list += self.new_position(self.date, fut, opt_chain)
            return trans_list

    def log(self, message):
        if self.console_logging:
            logging.info(message)
        else:
            super().log(message)