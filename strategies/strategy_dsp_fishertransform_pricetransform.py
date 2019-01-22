from sklearn import preprocessing
from backtester.strategy import StrategyBase
import numpy as np


class Strategy_DSP_FisherTransform_PriceTransform(StrategyBase):
    name = 'Strategy_DSP_FisherTransform_PriceTransform'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    def calc_entryexit_rules(self, ma_period, scaling_window_period, transform_with, rules_index):
        px_ser = self.data.exo

        def universal_fisher_transform(series, scaling_period, transform_with='arctanh'):
            '"transform_with" options - "tanh", "arctanh"'

            # Centering the series
            series = series.rolling(int(scaling_period / 2)).apply(lambda x:
                                                                   preprocessing.StandardScaler().fit_transform(
                                                                       x.reshape(-1, 1)
                                                                       ).ravel()[-1])

            # limiting it to -0.999 > x < 0.999
            series = series.rolling(int(scaling_period / 2)).apply(lambda x:
                                                                   preprocessing.MinMaxScaler(
                                                                       feature_range=(-0.999, 0.999)
                                                                       ).fit_transform(x.reshape(-1, 1)).ravel()[-1])

            if transform_with == 'arctanh':
                ft_ser = np.arctanh(series)
                # ft_ser += 0.25 * ft_ser.shift(1)
                # ft_ser += 0.5 * ft_ser.shift(1)

            elif transform_with == 'tanh':
                ft_ser = np.tanh(series)
                # ft_ser += 0.25 * ft_ser.shift(1)
                # ft_ser += 0.5 * ft_ser.shift(1)

            return ft_ser

        ft_ser = universal_fisher_transform(px_ser.rolling(ma_period).mean(),
                                            scaling_window_period, transform_with=transform_with)

        if rules_index == 0:
            entry_rule = ft_ser > ft_ser.shift(1)
            exit_rule = ft_ser < ft_ser.shift(1)

            return entry_rule, exit_rule

        elif rules_index == 1:
            entry_rule = ft_ser < ft_ser.shift(1)
            exit_rule = ft_ser > ft_ser.shift(1)

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
            direction, ma_period, scaling_window_period, transform_with, rules_index = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, ma_period, scaling_window_period, transform_with, rules_index = params

        # Defining EXO price
        px = self.data.exo

        entry_rule, exit_rule = self.calc_entryexit_rules(ma_period, scaling_window_period, transform_with, rules_index)

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None

        return swarm_member_name, entry_rule, exit_rule, calc_info