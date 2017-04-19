from backtester.strategy import StrategyBase
from scipy import signal
import pandas as pd
from backtester.analysis import *


class Strategy_DSP_InstaTrendline(StrategyBase):
    name = 'Strategy_DSP_InstaTrendline'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    def calc_entryexit_rules(self, direction, alpha, alpha_trail, rules_index):
        px_ser = self.data.exo

        def instant_lowpass(series, a):
            ilp = pd.Series(index=series.index)

            ser_shift1 = series.shift(1)
            ser_shift2 = series.shift(2)

            for i in range(series.size):
                if i < 7:
                    ilp.iloc[i] = (series.iloc[i] + 2 * ser_shift1.iloc[i] + ser_shift2.iloc[i]) / 4

                else:
                    ilp.iloc[i] = ((a - a * a / 4) * series.iloc[i] + 0.5 * a * a * ser_shift1.iloc[i] -
                                   (a - 0.75 * a * a) * ser_shift2.iloc[i] + 2 * (1 - a) *
                                   ilp.shift(1).iloc[i] - (1 - a) * (1 - a) * ilp.shift(2).iloc[i])

            return ilp

        it = instant_lowpass(px_ser, alpha)
        it_trail = instant_lowpass(px_ser, alpha_trail)

        if rules_index == 0:
            entry_rule = it > px_ser

            if direction == 1:
                exit_rule = (it < px_ser) | (CrossDown(px_ser, it_trail))

            elif direction == -1:
                exit_rule = (it < px_ser) | (CrossUp(px_ser, it_trail))

            return entry_rule, exit_rule

        elif rules_index == 1:
            entry_rule = it < px_ser

            if direction == 1:
                exit_rule = (it > px_ser) | (CrossDown(px_ser, it_trail))

            elif direction == -1:
                exit_rule = (it > px_ser) | (CrossUp(px_ser, it_trail))

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
            direction, alpha, alpha_trail, rules_index = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, alpha, alpha_trail, rules_index = params

        entry_rule, exit_rule = self.calc_entryexit_rules(direction, alpha, alpha_trail, rules_index)

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None

        return swarm_member_name, entry_rule, exit_rule, calc_info