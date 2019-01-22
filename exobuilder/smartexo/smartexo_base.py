from exobuilder.exo.exoenginebase import ExoEngineBase
from exobuilder.algorithms.rollover_helper import RolloverHelper
import logging

class SmartEXOBase(ExoEngineBase):
    EXO_NAME = "SmartEXOBase"

    def __init__(self, symbol, direction, date, datasource, **kwargs):
        self._symbol = symbol
        self.custom_values = {}

        # Use ContFut EXO to process SmartEXO data
        self._base_exo_name = "{0}_ContFut".format(self._symbol)

        super().__init__(symbol, direction, date, datasource, **kwargs)

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
            for p in self.position.legs.values():
                rh = RolloverHelper(p.instrument)
                if rh.is_rollover(p):
                    return True
        return False

    def process_rollover(self):
        trans_list = self.position.close_all_translist()
        self.log('Rollover occured, new series used')
        return trans_list

    def get_custom_values(self):
        """
        Method that return custom EXO data frame values, to store inside EXO Dataframe in the DB
        :return: dictionary {'string_key': (int or float) value}
        """
        return self.custom_values

    def calculate_regime(self, date, exo_df):
        """
        Calculates Bull/Bear/Neutral areas based on some logic

        :param date: Current date time
        :param exo_df: Price dataframe for underlying quotes
        :return:
        -1 - for bearish zone
        0  - for neutral zone
        +1 - for bullish zone
        None - for unknown (just lead to existing position close)
        """
        raise NotImplementedError("You should override this method to process SmartEXO logic")

    @staticmethod
    def new_position_bullish_zone(date, fut, opt_chain):
        """
        Returns transaction to open new Smart EXO position for bullish zone

        params date: current date
        params fut: current actual future contract
        params opt_chain: current actual options chain

        returns: List of Transactions to open
        """
        return []

    @staticmethod
    def new_position_bearish_zone(date, fut, opt_chain):
        """
        Returns transaction to open new Smart EXO position for bearish zone

        params date: current date
        params fut: current actual future contract
        params opt_chain: current actual options chain

        returns: List of Transactions to open
        """
        return []

    @staticmethod
    def new_position_neutral_zone(date, fut, opt_chain):
        """
        Returns transaction to open new Smart EXO position for neutral zone

        params date: current date
        params fut: current actual future contract
        params opt_chain: current actual options chain

        returns: List of Transactions to open
        """
        return []


    def manage_opened_position(self, date, fut, opt_chain, regime, opened_position):
        """
        Return transactions list to manage opened positions, it could be used for delta rebalancing or dynamic delta hedging

        :param fut:
        :param opt_chain:
        :param regime:
        :param opened_position:
        :return:
        """
        return []

    def process_day(self):
        """
        Main EXO's position management method
        :return: list of Transactions to process
        """

        # Get cont futures price for EXO
        exo_df, exo_info = self.datasource.exostorage.load_series(self._base_exo_name)

        regime = self.calculate_regime(self.date, exo_df)

        logging.debug("Regime {0}".format(regime))

        trans_list = []

        #
        # Writing custom values to store inside DB
        #
        self.custom_values = {
            'regime': regime if regime is not None else float('nan')
        }

        if regime is None and len(self.position) > 0:
            return self.position.close_all_translist()

        instr = self.datasource.get(self._symbol, self.date)
        rh = RolloverHelper(instr)
        fut, opt_chain = rh.get_active_chains()

        if fut is None or opt_chain is None:
            raise ValueError("Active option chain is not found for {0}".format(self._symbol))

        if regime == 1 and 'bullish' not in self.position.legs:
            # Close all
            trans_list += self.position.close_all_translist()
            tl = self.new_position_bullish_zone(self.date, fut, opt_chain)

            if len(tl) > 0:
                tl[0]._leg_name = 'bullish'
                trans_list += tl
            self._log_transactions(trans_list)
            return trans_list

        if regime == -1 and 'bearish' not in self.position.legs:
            # Close all
            trans_list += self.position.close_all_translist()
            tl = self.new_position_bearish_zone(self.date, fut, opt_chain)

            if len(tl) > 0:
                tl[0]._leg_name = 'bearish'
                trans_list += tl
            self._log_transactions(trans_list)
            return trans_list

        if regime == 0 and 'neutral' not in self.position.legs:
            # Close all
            trans_list += self.position.close_all_translist()
            tl = self.new_position_neutral_zone(self.date, fut, opt_chain)

            if len(tl) > 0:
                tl[0]._leg_name = 'neutral'
                trans_list += tl
            self._log_transactions(trans_list)
            return trans_list



        #
        # Manage opened position
        #
        return self.manage_opened_position(self.date, fut, opt_chain, regime, self.position)
