import os
import itertools
import numpy as np
import pandas as pd
from multiprocessing import Pool
from backtester import matlab
from backtester.exoinfo import EXOInfo

import pyximport;
pyximport.install(setup_args={"include_dirs": np.get_include()})
from backtester import backtester
from backtester.backtester_fast import backtest, stats_exposure

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

    def __str__(self):
        return "OptParam('{0}', min={1}, max={2}, step={3})".format(self.name, self.min, self.max, self.step)

class OptParamArray(object):
    """
    Generic system optimization parameter, like Moving Avg period etc..
    """
    def __init__(self, name, array):
        self.name = name
        self.array = array

    def __str__(self):
        return "OptParamArray('{0}', {1})".format(self.name, self.array)


class StrategyBase(object):
    """
    Base class for swarming strategy
    """
    name = 'BaseStrategy'

    def __init__(self, strategy_context):
        self.opts = None
        self.costs = None

        # Checking context integrity
        self.check_context(strategy_context)
        self.context = strategy_context


        self.exo_name = strategy_context['strategy']['exo_name']
        self.load_exodata()

        self.exoinfo = EXOInfo(self.data, self.exo_dict)

        self.global_filter = None
        self.global_filter_data = None
        self._filtered_swarm = None
        self._filtered_swarm_equity = None
        #
        # Set costs
        #
        if 'costs' in self.context:
            self.init_costs()

    def init_costs(self):
        cost_manager = self.context['costs']['manager'](self.exo_dict, self.context)
        self.costs = cost_manager.get_costs(self.data.exo)

    def load_exodata(self):
        if 'exo_storage' in self.context['strategy']:
            storage = self.context['strategy']['exo_storage']
            self.data, self.exo_dict = storage.load_series(self.exo_name)
            if self.data is None:
                raise KeyError("EXO ('{0}') not found in EXOStorage engine".format(self.exo_name))
            del self.context['strategy']['exo_storage']
        else:
            if os.path.exists(self.exo_name):
                self.data, self.exo_dict = matlab.loaddata(self.exo_name)
            else:
                TMQRPATH = os.getenv("TMQRPATH", '')
                self.data, self.exo_dict = matlab.loaddata(os.path.join(TMQRPATH, 'mat', self.exo_name.replace('.mat', '') + '.mat'))

    def check_context(self, context):
        if 'strategy' not in context:
            raise KeyError('"strategy" settings not found')

        strategy_settings = context['strategy']

        if 'class' not in strategy_settings:
            raise KeyError('"class" settings not found in strategy settings')
        if 'exo_name' not in strategy_settings:
            raise KeyError('"exo_name" settings not found in strategy settings')
        if 'opt_params' not in strategy_settings:
            raise KeyError('"opt_params" settings not found in strategy settings')

        if 'costs' in context:
            #
            # Check the costs manager settings
            #
            if 'manager' not in context['costs']:
                raise KeyError('"manager" settings not found in strategy settings')

    def get_member_name(self, opt_param):
        return str(opt_param)

    def slice_opts(self):
        opts = self.context['strategy']['opt_params']
        if opts is None:
            return [None]

        if 'opt_preset' in self.context['strategy']:
            return self.context['strategy']['opt_preset']

        result = []
        for o in opts:
            if type(o) == OptParam:
                # Including last step in sample
                result.append(np.arange(o.min, o.max+o.step, o.step))
            elif type(o) == OptParamArray:
                result.append(o.array)
            else:
                raise Exception('Unexpected OptParam type')

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
        raise NotImplementedError("Method 'default_opts' is obsolete")

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

        # In bi-directional mode 1-st opt argument must be *direction* of the swarm
        direction = opts[0]
        if direction != 1 and direction != -1:
            raise Exception('In bi-direction mode fist opt argument must be Direction: 1 or -1')

        swarm_name, entry_rule, exit_rule, calc_info = self.calculate(opts)

        # Backtesting routine
        pl, inposition = backtest(self.data, entry_rule.values, exit_rule.values, direction)
        #pl, inposition = backtester.backtest(self.data, entry_rule, exit_rule, direction)


        # Apply global filter to trading system entries
        if self._filtered_swarm is not None:
            filtered_inpos = self._filtered_swarm[self.get_member_name(opts)]

            # Binary AND to arrays
            if self.global_filter is not None:
                inposition = inposition & filtered_inpos & self.global_filter
            else:
                inposition = inposition & filtered_inpos

        # Do backtest (exposure based)
        # Exposure Direction * PositionSize * InPositionFlag
        exposure = inposition.astype(np.uint8) * float(direction) * self.positionsize

        # Do quick backtest (equity line only without stats)
        equity, stats_dict = stats_exposure(self.data, exposure, self.costs, extendedstats=False)

        return (swarm_name, equity, exposure, inposition)


    def run_swarm_backtest(self, filtered_swarm=None, filtered_swarm_equity=None):
        '''
        Brute force all steps of self.opts and calculate base stats
        '''
        result = {}
        result_exposure = {}
        result_inpos = {}

        # Storing temporary filter state
        self._filtered_swarm = filtered_swarm
        self._filtered_swarm_equity = filtered_swarm_equity

        #
        # Calculating global filter function if available
        #
        if filtered_swarm is not None and 'swarm' in self.context:
            swarm_settings = self.context['swarm']
            if 'global_filter_function' in swarm_settings:
                gf_func = swarm_settings['global_filter_function']
                params = None
                if 'global_filter_params' in swarm_settings:
                    params = swarm_settings['global_filter_params']
                self.global_filter, self.global_filter_data = gf_func(filtered_swarm_equity, params)

        opts_list = self.slice_opts()

        pool = Pool()
        pool_results = pool.map(self._calc_swarm_member, opts_list)

        for pool_res in pool_results:
            swarm_name, equity, swarm_exposure, inposition = pool_res
            result[swarm_name] = equity
            result_exposure[swarm_name] = swarm_exposure
            result_inpos[swarm_name] = inposition

        pool.close()
        pool.join()

        self._filtered_swarm = None

        return pd.DataFrame.from_dict(result), pd.DataFrame.from_dict(result_exposure), pd.DataFrame.from_dict(result_inpos, dtype=np.int8)

    def calculate(self, params=None, save_info=False):
        """
        The main method for trading logics calculation
        :param direction: direction of the swarm member
        :param params: tuple-like object with optimizations parameters
        :param save_info: store calculation information for strategy
        :return:
        tripple (swarm_member_name, entry_rule, exit_rule)
        """
        return None, None, None, None
