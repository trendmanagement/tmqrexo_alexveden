import itertools
import numpy as np
import pandas as pd
from backtester import backtester

class OptParam(object):
    """
    Generic system optimization parameter, like Moving Avg period etc..
    """
    def __init__(self, name, default_value, min_value, max_value, step):
        self.name = name
        self.default = default_value
        self.min = min_value
        self.max = max_value
        self.step = step


class StrategyBase(object):
    """
    Base class for swarming strategy
    """
    def __init__(self):
        self.name = 'BaseStrategy'
        self.opts = None
        self.direction = 0
        self.costs = None


    def slice_opts(self):
        if self.opts is None:
            return [None]
        result = []
        for o in self.opts:
            result.append(np.arange(o.min, o.max, o.step))
        return itertools.product(*result)

    def default_opts(self):
        """
        Returns default tuple params for opts
        :return:
        """
        if self.opts is None:
            return None
        results = []

        for o in self.opts:
            results.append(o.default)
        return tuple(results)

    @property
    def positionsize(self):
        """
        Returns volatility adjuster positions size for strategy
        :return:
        """
        # Defining EXO price
        px = self.data.exo

        # Calculate position size adjusted to volatility of EXO
        # Dollar risk per 1 volatility unit
        risk_perunit = 100
        risk_vola_period = 100

        # Calculate volatility unit
        # In this case we use 10-period rolling median of EXO changes
        vola = abs(px.diff()).rolling(risk_vola_period).median()
        # We want to risk 100$ per 1 volatility unit
        #
        # This type of position sizing used for calibration of swarm members
        # After swarm generation and picking we will use portfolio based MM by Van Tharp
        # Tailored for portfolio size and risks of particular client
        return risk_perunit / vola

    def run_swarm(self):
        '''
        Brute force all steps of self.opts and calculate base stats
        '''
        result = {}
        result_stats = {}
        result_inpos = {}

        # Get position size (vola adjusted)
        # All portfolio sizing will be done in the future steps
        vola_adjusted_size = self.positionsize


        for opts in self.slice_opts():
            #
            # Calculation trading system rules
            #
            swarm_name, entry_rule, exit_rule = self.calculate(opts)


            # Backtesting routine
            pl, inposition = backtester.backtest(self.data, entry_rule, exit_rule, self.direction)
            equity, stats = backtester.stats(pl, inposition, vola_adjusted_size, self.costs)

            # Storing swarm in the dictionary
            result[swarm_name] = equity
            result_stats[swarm_name] = stats
            result_inpos[swarm_name] = inposition

        return pd.DataFrame.from_dict(result), pd.DataFrame.from_dict(result_stats, dtype=np.float).T, pd.DataFrame.from_dict(result_inpos, dtype=np.int8)

    def calculate(self, params=None):
        """
        The main method for trading logics calculation
        :param params: tuple-like object with optimizations parameters
        :return:
        tripple (swarm_member_name, entry_rule, exit_rule)
        """
        return None, None, None
