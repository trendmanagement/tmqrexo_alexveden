from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam


class Strategy_TurtlesBreakouts_w_PosSizing(StrategyBase):
    name = 'Strategy_TurtlesBreakouts_w_PosSizing'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    @property
    def positionsize(self):
        """
        Returns volatility adjuster positions size for strategy
        :return:
        """

        px_ser = self.data.exo
        # H = L = C = px_ser
        # atr = ATR(H, L, C, 20)

        return pd.Series(1.0, index=px_ser.index)
        # return ((20**4)*0.01 / atr).round().fillna(0.0)

    def calc_entryexit_rules(self, H, L, C, atr_period, rolling_min_max_period, rules_index):

        px_ser = self.data.exo
        H = L = C = px_ser

        #atr = ATR(H, L, C, atr_period)

        if rules_index == 0:
            entry_rule = CrossDown(px_ser, px_ser.rolling(rolling_min_max_period).min() + 1)

            exit_rule = CrossUp(px_ser, px_ser.rolling(np.max([2, int(rolling_min_max_period / 2)])).max() - 1)
            return entry_rule, exit_rule

        if rules_index == 1:
            entry_rule = CrossUp(px_ser, px_ser.rolling(rolling_min_max_period).max() - 1)

            exit_rule = CrossDown(px_ser, px_ser.rolling(np.max([2, int(rolling_min_max_period / 2)])).min() + 1)
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
            direction, atr_period, rolling_min_max_period, rules_index = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, atr_period, rolling_min_max_period, rules_index = params

        # Defining EXO price
        px = self.data.exo

        H = L = C = px

        # Enry/exit rules
        entry_rule, exit_rule = self.calc_entryexit_rules(H, L, C, atr_period, rolling_min_max_period, rules_index)

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None
        #if save_info:
        #    calc_info = {'trailing_stop': trailing_stop}

        return swarm_member_name, entry_rule, exit_rule, calc_info