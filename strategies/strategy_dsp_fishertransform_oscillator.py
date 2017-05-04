from sklearn import (pipeline, preprocessing, ensemble, neighbors, model_selection)
from backtester.strategy import StrategyBase
import pandas as pd

class Strategy_DSP_FisherTransform_Oscillator(StrategyBase):
    name = 'Strategy_DSP_FisherTransform_Oscillator'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    def calc_entryexit_rules(self, ft_period, rules_index):
        px_ser = self.data.exo

        def fisher_transform_osc(c, period, h=None, l=None):
            if (h == None) & (l == None):
                c = c
                h = c
                l = c

            period = period

            max_h = h.rolling(period).max()
            min_l = l.rolling(period).min()

            indicator = pd.Series(index=c.index)  # looks like stochastic

            for i in c.index:
                indicator.loc[i] = max(-0.9999, min(0.9999, 0.5 * 2 * (
                (c.ix[i] - min_l.ix[i]) / (max_h.ix[i] - min_l.ix[i]) - 0.5)))

            indicator += 0.5 * indicator.shift(1)

            fish_t = 0.25 * np.log((1 + indicator) / (1 - indicator))
            fish_t += 0.5 * fish_t.shift(1)

            return fish_t

        if rules_index == 0:
            ft_osc = fisher_transform_osc(px_ser, ft_period)

            entry_rule = ft_osc > ft_osc.shift(1)
            exit_rule = ft_osc < ft_osc.shift(1)

            return entry_rule, exit_rule

        elif rules_index == 1:
            ft_osc = fisher_transform_osc(px_ser, ft_period)

            entry_rule = ft_osc < ft_osc.shift(1)
            exit_rule = ft_osc > ft_osc.shift(1)

            return entry_rule, exit_rule

        elif rules_index == 2:
            ft_osc = fisher_transform_osc(px_ser, ft_period)

            entry_rule = (ft_osc > 0) & (ft_osc.shift(1) < 0)
            exit_rule = (ft_osc < 0) & (ft_osc.shift(1) > 0)

            return entry_rule, exit_rule

        elif rules_index == 3:
            ft_osc = fisher_transform_osc(px_ser, ft_period)

            entry_rule = (ft_osc < 0) & (ft_osc.shift(1) > 0)
            exit_rule = (ft_osc > 0) & (ft_osc.shift(1) < 0)

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
            direction, ft_period, rules_index = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, ft_period, rules_index = params

        # Defining EXO price
        px = self.data.exo

        entry_rule, exit_rule = self.calc_entryexit_rules(ft_period, rules_index)

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None

        return swarm_member_name, entry_rule, exit_rule, calc_info