import numpy as np
import pandas as pd
from backtester.strategy import StrategyBase
from scipy import signal


class Strategy_KeltChannelLP(StrategyBase):
    name = 'Strategy_KeltChannelLP'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    def calc_entryexit_rules(self, window_period, n_lags, rules_index):

        px_ser = self.data.exo

        def lp_filter(series, filt_order, filt_freq):
            series = series.copy()
            b, a = signal.butter(filt_order, filt_freq, btype='lowpass')

            series.loc[:] = signal.lfilter(b, a, series)

            return series

        ma_periods = window_period
        periods_to_alpha = max(0.0, 2 / (ma_periods + 1))

        # typical_px = (ohlc.h + ohlc.l + ohlc.c) / 3.0
        typical_avg = lp_filter(self.data.exo, 1, periods_to_alpha)

        lp_freqs = np.arange(periods_to_alpha / 4, periods_to_alpha * 2, periods_to_alpha / 4)
        lp_df = pd.DataFrame(index=typical_avg.index)

        for f in lp_freqs:
            lp_df['lp_freq{:0.2f}'.format(f)] = lp_filter(typical_avg, 1, f)

        consensus = (lp_df >= lp_df.shift(1)).mean(1)

        lags = n_lags
        for i in range(1, lags):
            consensus += (lp_df >= lp_df.shift(i)).mean(1)

        consensus /= lags

        keltner_direction = (consensus > consensus.shift()) | (consensus == 0.60)

        if rules_index == 0:
            entry_rule = keltner_direction == True
            exit_rule = keltner_direction == False

            return entry_rule, exit_rule

        if rules_index == 1:
            entry_rule = keltner_direction == False
            exit_rule = keltner_direction == True

            return entry_rule, exit_rule

        elif rules_index == 2:
            entry_rule = consensus > consensus.shift()
            exit_rule = consensus < consensus.shift()

            return entry_rule, exit_rule

        elif rules_index == 3:
            entry_rule = consensus < consensus.shift()
            exit_rule = consensus > consensus.shift()

            return entry_rule, exit_rule

        elif rules_index == 4:
            entry_rule = consensus == 1.0
            exit_rule = consensus == 0.0

            return entry_rule, exit_rule

        elif rules_index == 5:
            entry_rule = consensus == 0.0
            exit_rule = consensus == 1.0

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
            direction, window_period, n_lags, rules_index = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, window_period, n_lags, rules_index = params

            # Defining EXO price
        px = self.data.exo

        # Enry/exit rules
        entry_rule, exit_rule = self.calc_entryexit_rules(window_period, n_lags, rules_index)

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None
        # if save_info:
        #     calc_info = {'trailing_stop': trailing_stop}

        return swarm_member_name, entry_rule, exit_rule, calc_info
