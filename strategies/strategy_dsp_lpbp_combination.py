from sklearn import (pipeline, preprocessing, ensemble, neighbors, model_selection)
from scipy import signal, ndimage
from backtester.analysis import *
from backtester.strategy import StrategyBase



class Strategy_DSP_LPBP_Combination(StrategyBase):
    name = 'Strategy_DSP_LPBP_Combination'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    def calc_entryexit_rules(self, lp_order, lp_freq, bp_order, bp_startfreq, bp_stopfreq, bp_multiplier, rule_index):
        px_ser = self.data.exo

        b, a = signal.butter(lp_order, lp_freq, btype='lowpass')

        lpfilt = px_ser.copy()
        lpfilt.values[:] = signal.lfilter(b, a, lpfilt)

        b, a = signal.butter(bp_order, [bp_startfreq, bp_stopfreq], btype='bandpass')

        bpfilt = px_ser.copy()
        bpfilt.values[:] = signal.lfilter(b, a, bpfilt)

        lpbp = lpfilt - bpfilt * bp_multiplier

        if rule_index == 0:
            entry_rule = CrossDown(lpbp, px_ser)
            exit_rule = CrossUp(lpbp, px_ser)

            return entry_rule, exit_rule

        elif rule_index == 1:
            entry_rule = CrossUp(lpbp, px_ser)
            exit_rule = CrossDown(lpbp, px_ser)

            return entry_rule, exit_rule

        elif rule_index == 2:
            entry_rule = lpbp > lpfilt
            exit_rule = lpbp < lpfilt

            return entry_rule, exit_rule

        elif rule_index == 3:
            entry_rule = lpbp < lpfilt
            exit_rule = lpbp > lpfilt

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
            (direction, lp_order, lp_freq, bp_order, bp_startfreq, bp_stopfreq, bp_multiplier,
             rule_index) = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            (direction, lp_order, lp_freq, bp_order, bp_startfreq, bp_stopfreq, bp_multiplier, rule_index) = params

        # Defining EXO price
        px = self.data.exo

        entry_rule, exit_rule = self.calc_entryexit_rules(lp_order, lp_freq, bp_order, bp_startfreq,
                                                          bp_stopfreq, bp_multiplier, rule_index)

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None

        return swarm_member_name, entry_rule, exit_rule, calc_info