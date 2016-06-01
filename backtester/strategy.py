import os
import itertools
import numpy as np
import pandas as pd
from backtester import backtester
from multiprocessing import Pool
from backtester import matlab
from backtester.exoinfo import EXOInfo

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
    def __init__(self, strategy_context):
        self.name = 'BaseStrategy'
        self.opts = None
        self.direction = 0
        self.costs = None
        self.context = strategy_context

        self.check_context()

        self.exo_name = strategy_context['strategy']['exo_name']

        self.load_exodata()

        self.exoinfo = EXOInfo(self.data, self.exo_dict)
        #
        # Set costs
        #
        if 'costs' in self.context:
            cost_manager = self.context['costs']['manager'](self.exo_dict, self.context)
            self.costs = cost_manager.get_costs(self.data.exo)

    def load_exodata(self):
        if os.path.exists(self.exo_name):
            self.data, self.exo_dict = matlab.loaddata(self.exo_name)
        else:
            self.data, self.exo_dict = matlab.loaddata('../mat/' + self.exo_name + '.mat')

    def check_context(self):
        if 'strategy' not in self.context:
            raise ValueError('"strategy" settings not found')

        strategy_settings = self.context['strategy']

        if 'exo_name' not in strategy_settings:
            raise ValueError('"exo_name" settings not found in strategy settings')
        if 'direction' not in strategy_settings:
            raise ValueError('"direction" settings not found in strategy settings')
        if 'opt_params' not in strategy_settings:
            raise ValueError('"opt_params" settings not found in strategy settings')

        if 'costs' in self.context:
            #
            # Check the costs manager settings
            #
            if 'manager' not in self.context['costs']:
                raise ValueError('"manager" settings not found in strategy settings')

    def get_member_name(self, opt_param):
        return str(opt_param)

    def slice_opts(self):
        if self.opts is None:
            return [None]
        result = []
        for o in self.opts:
            # Including last step in sample
            result.append(np.arange(o.min, o.max+o.step, o.step))
        params_universe = itertools.product(*result)

        #
        #   Filtering params universe according to picked swarm members
        #
        if self._filtered_swarm is not None:
            filtered_universe = []
            for p in params_universe:
                if self.get_member_name(p) in self._filtered_swarm:
                    filtered_universe.append(p)
            return filtered_universe

        return params_universe

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
        return pd.Series(1, index=px.index)

    def _calc_swarm_member(self, opts):
        swarm_name, entry_rule, exit_rule, calc_info = self.calculate(opts)

        # Backtesting routine
        pl, inposition = backtester.backtest(self.data, entry_rule, exit_rule, self.direction)

        if self._filtered_swarm is not None:
            filtered_inpos = self._filtered_swarm[self.get_member_name(opts)]
            # Apply global filter to trading system entries
            # Binary AND to arrays
            inposition = inposition & filtered_inpos

        equity, stats = backtester.stats(pl, inposition, self.positionsize, self.costs)

        return (swarm_name, equity, stats, inposition)

    def run_swarm(self, filtered_swarm=None):
        '''
        Brute force all steps of self.opts and calculate base stats
        '''
        result = {}
        result_stats = {}
        result_inpos = {}

        # Storing temporary filter state
        self._filtered_swarm = filtered_swarm

        opts_list = self.slice_opts()

        pool = Pool()
        pool_results = pool.map(self._calc_swarm_member, opts_list)

        for pool_res in pool_results:
            swarm_name, equity, stats, inposition = pool_res
            result[swarm_name] = equity
            result_stats[swarm_name] = stats
            result_inpos[swarm_name] = inposition

        pool.close()
        pool.join()

        self._filtered_swarm = None

        return pd.DataFrame.from_dict(result), pd.DataFrame.from_dict(result_stats, dtype=np.float).T, pd.DataFrame.from_dict(result_inpos, dtype=np.int8)

    def calculate(self, params=None, save_info=False):
        """
        The main method for trading logics calculation
        :param params: tuple-like object with optimizations parameters
        :param save_info: store calculation information for strategy
        :return:
        tripple (swarm_member_name, entry_rule, exit_rule)
        """
        return None, None, None
