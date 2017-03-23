from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.tests.assetindexdict import AssetIndexDicts
from datetime import datetime, date, timedelta, time as dttime
from exobuilder.contracts.instrument import Instrument
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.datasource_sql import DataSourceSQL
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.exostorage import EXOStorage
from exobuilder.exo.exoenginebase import ExoEngineBase
from exobuilder.exo.transaction import Transaction
import time
from exobuilder.algorithms.rollover_helper import RolloverHelper

class EXOBrokenwingCollar(ExoEngineBase):
    def __init__(self, symbol, direction, date, datasource, log_file_path=''):
        self._direction = direction
        self._symbol = symbol

        if self._direction != 1 and self._direction != -1:
            raise ValueError('self._direction != 1 and self._direction != -1')

        super().__init__(symbol, direction, date, datasource, log_file_path=log_file_path)

    @staticmethod
    def direction_type():
        return 0

    @staticmethod
    def names_list(symbol):
        return [symbol + '_BullishCollarBW', symbol + '_BearishCollarBW']

    @property
    def exo_name(self):
        if self._direction == 1:
            return self._symbol + '_BullishCollarBW'
        elif self._direction == -1:
            return self._symbol + '_BearishCollarBW'

    def is_rollover(self):
        if len(self.position) != 0:
            for p in self.position.legs.values():
                rh = RolloverHelper(p.instrument)
                if rh.is_rollover(p):
                    return True
        return False

    def process_rollover(self):
        trans_list = self.position.close_all_translist()
        return trans_list


    def process_day(self):
        """
        Main EXO's position management method
        :return: list of Transactions to process
        """


        if len(self.position) == 0:
            instr = self.datasource.get(self._symbol, self.date)
            rh = RolloverHelper(instr)
            fut, opt_chain = rh.get_active_chains()
            if fut is None or opt_chain is None:
                if self.debug_mode:
                    self.logger.write(
                        'Futures contract or option chain not found.\n\tFuture: {0}\tOption chain: {1}\n'.format(
                            fut,
                            opt_chain
                        ))
                return []

            if self._direction == 1:
                # the bullish broken wings are long the -5 put , long the future, short the  + 5 call and long the +9 call
                put_dn5 = opt_chain[-5].P
                call_up5 = opt_chain[5].C
                call_up9 = opt_chain[9].C


                return [
                    Transaction(put_dn5, self.date, 1.0, put_dn5.price, leg_name='opt_otm_leg'),
                    Transaction(fut, self.date, 1.0, fut.price, leg_name='fut_leg'),
                    Transaction(call_up5, self.date, -1.0, call_up5.price, leg_name='call_up5_short_leg'),
                    Transaction(call_up9, self.date, 1.0, call_up9.price, leg_name='call_up9_long_leg'),
                ]
            if self._direction == -1:
                # the bearish BW  long the -9 put, short the -5 put , short the future, long the + 5 call
                call_up5 = opt_chain[5].C
                put_dn9 = opt_chain[-9].P
                put_dn5 = opt_chain[-5].P

                return [
                    Transaction(call_up5, self.date, 1.0, call_up5.price, leg_name='opt_otm_leg'),
                    Transaction(fut, self.date, -1.0, fut.price, leg_name='fut_leg'),
                    Transaction(put_dn9, self.date, 1.0, put_dn9.price, leg_name='put_dn9_long_leg'),
                    Transaction(put_dn5, self.date, -1.0, put_dn5.price, leg_name='put_dn5_short_leg'),
                ]
