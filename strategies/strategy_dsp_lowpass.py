from scipy import signal
from backtester.analysis import *
from backtester.strategy import StrategyBase


class Strategy_DSP_LowPass(StrategyBase):
    name = 'Strategy_DSP_LowPass'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    def calc_entryexit_rules(self, filt1_order, filt1_freq, filt2_order, filt2_freq, rule_index):
        px_ser = self.data.exo

        b, a = signal.butter(filt1_order, filt1_freq, btype='lowpass')

        filt1 = px_ser.copy()
        filt1.values[:] = signal.lfilter(b, a, filt1)

        b, a = signal.butter(filt2_order, filt2_freq, btype='lowpass')

        filt2 = px_ser.copy()
        filt2.values[:] = signal.lfilter(b, a, filt2)

        if rule_index == 0:
            entry_rule = CrossDown(filt1, filt2)
            exit_rule = CrossUp(filt1, filt2)

            return entry_rule, exit_rule

        elif rule_index == 1:
            entry_rule = CrossUp(filt1, filt2)
            exit_rule = CrossDown(filt1, filt2)

            return entry_rule, exit_rule

        if rule_index == 2:
            entry_rule = CrossDown(filt1, filt2)
            exit_rule = CrossUp(filt1, px_ser)

            return entry_rule, exit_rule

        elif rule_index == 3:
            entry_rule = CrossUp(filt1, filt2)
            exit_rule = CrossDown(filt1, px_ser)

            return entry_rule, exit_rule

        elif rule_index == 4:
            entry_rule = filt1 > filt2
            exit_rule = filt1 < filt2

            return entry_rule, exit_rule

        elif rule_index == 5:
            entry_rule = filt1 < filt2
            exit_rule = filt1 > filt2

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
            (direction, filt1_order, filt1_freq, filt2_order, filt2_freq, rule_index) = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            (direction, filt1_order, filt1_freq, filt2_order, filt2_freq, rule_index) = params

        # Defining EXO price
        px = self.data.exo

        entry_rule, exit_rule = self.calc_entryexit_rules(filt1_order, filt1_freq, filt2_order, filt2_freq, rule_index)

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None

        return swarm_member_name, entry_rule, exit_rule, calc_info