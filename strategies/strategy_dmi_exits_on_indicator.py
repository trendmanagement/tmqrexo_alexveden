from backtester.analysis import *
from backtester.strategy import StrategyBase
import pandas as pd
import numpy as np


class Strategy_DMI_exit_on_indicator_events(StrategyBase):
    name = 'DMI_exit_on_indicator'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)


    def calc_entryexit_rules(self, H, L, C,
                             dmi_period, rules_index, hl_data_available=False):
        px_ser = self.data.exo
        '''
        https://ru.tradingview.com/stock-charts-support/index.php/Directional_Movement_(DMI)

        Calculating the DMI can actually be broken down into two parts.
        First, calculating the +DI and -DI, and second, calculating the ADX.

        To calculate the +DI and -DI you need to find the +DM and -DM (Directional Movement).
        +DM and -DM are calculated using the High, Low and Close for each period.
        You can then calculate the following:

        Current High - Previous High = UpMove
        Current Low - Previous Low = DownMove

        If UpMove > DownMove and UpMove > 0, then +DM = UpMove, else +DM = 0
        If DownMove > Upmove and Downmove > 0, then -DM = DownMove, else -DM = 0

        Once you have the current +DM and -DM calculated, the +DM and -DM lines can be
        calculated and plotted based on the number of user defined periods.

        +DI = 100 times Exponential Moving Average of (+DM / Average True Range)
        -DI = 100 times Exponential Moving Average of (-DM / Average True Range)

        Now that -+DX and -DX have been calculated, the last step is calculating the ADX.

        ADX = 100 times the Exponential Moving Average of the Absolute Value of (+DI- -DI) / (+DI + -DI)'''

        #
        # Since there is no HL data, i will use a rolling max of C as High and rolling min of C as Low
        #

        if hl_data_available == False:
            H = L = C

        if hl_data_available == True:
            H = H
            L = L

        prev_high = H.shift(1)
        prev_low = L.shift(1)

        dm_pos = pd.Series(0.0, index=C.index)
        dm_neg = pd.Series(0.0, index=C.index)

        atr = ATR(H, L, C, dmi_period)

        for i in range(C.size):
            upmove = H[i] - prev_high[i]
            downmove = prev_low[i] - L[i]

            if (upmove > downmove) & (upmove > 0):
                dm_pos[i] = upmove

            if (downmove > upmove) & (downmove > 0):
                dm_neg[i] = downmove

        di_pos = ((dm_pos.rolling(dmi_period).mean() / atr).rolling(dmi_period).mean()) * 100
        di_neg = ((dm_neg.rolling(dmi_period).mean() / atr).rolling(dmi_period).mean()) * 100

        if rules_index == 0:
            entry_rule = CrossUp(di_pos, di_neg)

            exit_rule = CrossDown(di_pos, di_neg)
            return entry_rule, exit_rule

        if rules_index == 1:
            entry_rule = CrossUp(di_neg, di_pos)

            exit_rule = CrossDown(di_neg, di_pos)
            return entry_rule, exit_rule


    def calculate(self, params=None, save_info=False):
        #
        #
        #  Params is a tripple like (50, 10, 15), where:
        #   50 - slow MA period
        #   10 - fast MA period
        #   15 - median period
        #
        #  On every iteration of swarming algorithm, parameter set will be different.
        #  For more information look inside: /notebooks/tmp/Swarming engine research.ipynb
        #

        if params is None:
            # Return default parameters
            direction, dmi_period, rules_index = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, dmi_period, rules_index = params

        # Defining EXO price
        px = self.data.exo

        H = L = C = px

        # Enry/exit rules
        #
        # Since there is no HL data, i will use a rolling max of C as High and rolling min of C as Low
        # !!!  hl_data_available = False by default.
        #
        entry_rule, exit_rule = self.calc_entryexit_rules(H, L, C, dmi_period, rules_index)

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None

        return swarm_member_name, entry_rule, exit_rule, calc_info