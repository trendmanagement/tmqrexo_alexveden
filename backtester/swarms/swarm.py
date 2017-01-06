"""
TODO: brief description of swarm.py
"""

import numpy as np
import pandas as pd
import pickle
import os
from ast import literal_eval
import pyximport
pyximport.install(setup_args={"include_dirs": np.get_include()})

from backtester.backtester_fast import stats_exposure, calc_costs
from copy import  deepcopy
import inspect
import pprint
import warnings
from datetime import datetime
import warnings


class Swarm:
    def __init__(self, context, laststate=False):
        """
        Initialize picking engine with context
        :param context: dict(), strategy setting context
        :return:
        """
        self.context = context
        self.global_filter = None
        self._rebalancetime = None

        self._swarm = None
        self._swarm_stats = None
        self._swarm_inposition = None

        self._picked_swarm = None
        self._picked_inposition = None
        self._picked_exposure = None

        self._last_date = None
        self._last_exoquote = None
        self._last_exposure = None
        self._last_members_list = None
        self._last_rebalance_date = None
        self._last_delta = None
        self._last_prev_exposure = None
        self._max_exposure = None

        self._swarm_series = None
        self._delta = None

        self._islast_state = laststate

        strategy_settings = self.context['strategy']
        # Initialize strategy class
        self.strategy = strategy_settings['class'](self.context)

        self._swarm_avg = None
        self._swarm = None
        self._swarm_exposure = None



    @property
    def raw_equity(self):
        """
        Raw swarm cumulative equity (average swarm equity)
        :return:
        """
        if self._swarm_avg is None:
            raise ValueError("Run run_swarm() method before access this property")
        return self._swarm_avg

    @property
    def raw_swarm(self):
        """
        Raw swarm equities DataFrame
        :return:
        """
        if self._swarm is None:
            raise ValueError("Run run_swarm() method before access this property")
        return self._swarm

    @property
    def raw_inposition(self):
        """
        Raw swarm inposition flag
        :return:
        """
        if self._swarm_inposition is None:
            raise ValueError("Run run_swarm() method before access this property")
        return self._swarm_inposition

    @property
    def raw_exposure(self):
        """
        Raw swarm exposure = PositionSize * Direction * InPosition
        :return:
        """
        if self._swarm_exposure is None:
            raise ValueError("Run run_swarm() method before access this property")
        return self._swarm_exposure

    @property
    def picked_swarm(self):
        """
        Picked swarm equities DataFrame
        :return:
        """
        if self._picked_swarm is None:
            raise ValueError("Run pick() method before access this property")
        return self._picked_swarm

    @property
    def picked_inposition(self):
        """
        Picked swarm InPosition DataFrame
        :return:
        """
        if self._picked_inposition is None:
            raise ValueError("Run pick() method before access this property")
        return self._picked_inposition

    @property
    def picked_exposure(self):
        """
        Picked swarm exposure = PositionSize * Direction * InPosition
        :return:
        """
        if self._picked_exposure is None:
            raise ValueError("Run pick() method before access this property")
        return self._picked_exposure


    @property
    def picked_equity(self):
        """
        Net equity of picked swarm
        :return:
        """
        if self._swarm_series is None:
            raise ValueError("Run pick() method before access this property")
        return self._swarm_series['equity']

    @property
    def picked_stats(self):
        """
        Picked swarm base statistics
        :return:
        """
        if self._swarm_stats is None:
            raise ValueError("Run pick() method before access this property")
        return self._swarm_stats

    @property
    def picked_delta(self):
        """
        Cumulative delta of picked swarm members
        :return:
        """
        if self._swarm_series is None:
            raise ValueError("Run pick() method before access this property")

        return self._swarm_series['delta']

    @property
    def series(self):
        """
        Series for picked swarm result
        :return:
        """
        if self._swarm_series is None:
            raise ValueError("Run pick() method before access this property")

        return self._swarm_series


    @property
    def rebalancetime(self):
        """
        Rebalance time Series
        :return:
        """
        if self._rebalancetime is None:
            raise ValueError("Run pick() method before access this property")
        return self._rebalancetime

    def run_swarm(self):
        # Run strategy swarm
        self._swarm, self._swarm_exposure, self._swarm_inposition = self.strategy.run_swarm_backtest()
        #
        # Average swarm multiplied by members_count
        #   for reproduce comparable results 'picked_swarm' vs 'avg_swarm'
        eq_changes = self._swarm.diff()
        self._swarm_avg = eq_changes.mean(axis=1).cumsum() * self.context['swarm']['members_count']

    def pick(self):
        """
        Backtesting and swarm picking routine
        :param swarm:
        :return:
        """
        if self._islast_state:
            raise Exception("This swarm loaded from LastState Dict pick() it not applicable")

        swarm_settings = self.context['swarm']
        nSystems = swarm_settings['members_count']
        rankerclass = swarm_settings['ranking_class']

        self._rebalancetime = swarm_settings['rebalance_time_function'](self._swarm)

        picked_swarm_equity = np.zeros((len(self._swarm), nSystems))
        picked_swarm_inposition = np.zeros((len(self._swarm), nSystems))
        picked_swarm_exposure = np.zeros((len(self._swarm), nSystems))

        swarm_members = None
        swarm_members_next = None
        rebalance_info = []

        #
        # Clear ranking class cache if applicable
        #
        rankerclass.clear()

        for i in range(1, len(self._rebalancetime)):
            if swarm_members is not None and len(swarm_members) > 0:
                _swm_inposition = self._swarm_inposition[swarm_members]
                _swm_exposure = self._swarm_exposure[swarm_members]
                for j in range(len(swarm_members)):
                    # Add value-by-values to avoid cases when swarm members count < nSystems (exception raised)


                    # Store picked in position data
                    picked_swarm_inposition[i][j] = _swm_inposition.iat[i, j]

                    # Store swarm exposure in position data
                    picked_swarm_exposure[i][j] = _swm_exposure.iat[i, j]


            # == True - to avoid NaN values to pass condition
            if self._rebalancetime[i] == True:
                # To avoid future referencing in ranking functions use slicing
                swm_slice = self._swarm.iloc[:i + 1, :]

                # Pick new ranked swarm members
                #swarm_members, rank_info = ranker_14days(swm_slice, nSystems)
                swarm_members, rank_info = rankerclass.rank(swm_slice, nSystems)

                rebalance_info.append({
                    'rebalance_date': self._swarm.index[i],
                    'best_members': swarm_members,
                    'rank_info': rank_info
                })


        # Do backtest based on exposure stats
        for i in range(nSystems):
            _stats_dict = None
            series_df, _stats_dict = stats_exposure(self.strategy.data, picked_swarm_exposure[:, i], self.strategy.costs, extendedstats=False)
            picked_swarm_equity[:, i] = series_df['equity']

        self._picked_swarm = pd.DataFrame(picked_swarm_equity, self._swarm.index)
        self._picked_inposition = pd.DataFrame(picked_swarm_inposition, self._swarm.index)
        self._picked_exposure = pd.DataFrame(picked_swarm_exposure, self._swarm.index)
        self.rebalance_info = rebalance_info

        # Apply separate backtesting engine func
        #  due to position netting in the swarm we will have different costs
        #  Also store Extended stats dictionary for swarms statistics
        self._swarm_series, self._swarm_stats = stats_exposure(self.strategy.data, self.picked_exposure.sum(axis=1), self.strategy.costs, extendedstats=True)

        # Storing last state values used in online calculations
        self.fill_last_state()

    def fill_last_state(self):
        """
        Store last state values used in online calculations
        :return:
        """
        if len(self.picked_exposure) < 2 or len(self.rebalance_info) < 2:
            # Insufficient data
            raise RuntimeError("Swarm has less than 2 datapoints, check EXO quote to make sure that is enough data.")

        self._last_exposure = self.picked_exposure.iloc[-1].sum()
        self._last_prev_exposure = self.picked_exposure.iloc[-2].sum()
        self._last_date = self.picked_swarm.index[-1]
        self._last_members_list = self.rebalance_info[-1]['best_members']
        self._last_rebalance_date = self.rebalance_info[-1]['rebalance_date']
        self._last_exoquote = self.strategy.data['exo'].iloc[-1]
        self._last_delta = self.picked_delta.iloc[-1]



    @property
    def instrument(self):
        if '_' in self.exo_name:
            return self.exo_name.split('_')[0]

        return self.exo_name

    @property
    def exo_type(self):
        if '_' in self.exo_name:
            return self.exo_name.split('_')[1]

        return self.exo_name

    @property
    def exo_name(self):
        return self.strategy.exoinfo.exo_info['name']

    @property
    def direction(self):
        """
        Get alpha direction
        :return: tuple (int, str), (0|1|-1, 'Bidir'|'Long'|'Short')
        """
        return self.get_direction(self.context)

    @staticmethod
    def get_direction(strategy_context):
        """
        Get alpha direction from strategy_context
        :param strategy_context:
        :return: tuple (int, str), (0|1|-1, 'Bidir'|'Long'|'Short')
        """
        direction_param = strategy_context['strategy']['opt_params'][0]

        if 'direction' in strategy_context['strategy']:
            warnings.warn("'direction' parameter in strategy_context['strategy']['direction'] is obsolete, "
                          "please remove it to suppress this warning")

        if direction_param.name.lower() != 'direction':
            raise ValueError('First OptParam of strategy must be Direction')

        for dir_value in direction_param.array:
            if dir_value != -1 and dir_value != 1:
                raise ValueError("Direction OptParam value must be -1 or 1")

        if len(direction_param.array) == 1:
            if direction_param.array[0] == 1:
                return 1, 'Long'
            elif direction_param.array[0] == -1:
                return -1, 'Short'

        elif len(direction_param.array) == 2:
            return 0, 'Bidir'
        else:
            raise ValueError("Direction OptParam must contain 1 or 2 elements")



    @staticmethod
    def get_name(strategy_context, suffix=''):
        """
        Return swarm name based on strategy_context
        :param strategy_context:
        :param suffix: custom alpha suffix default: ''
        :return:
        """
        return '{0}_{1}_{2}{3}'.format(strategy_context['strategy']['exo_name'],
                                       Swarm.get_direction(strategy_context)[1],
                                       strategy_context['strategy']['class'].name,
                                       suffix)

    @property
    def name(self):
        """
        Return swarm manager human-readable name
        Underlying_EXOName_Strategy_Direction
        :return:
        """
        suffix = ''
        if 'suffix' in self.context['strategy'] \
                and self.context['strategy']['suffix'] is not None \
                and len(self.context['strategy']['suffix']) > 0:
            suffix = "_" + self.context['strategy']['suffix']

        return self.get_name(self.context, suffix)

    def save(self, directory,  filename=None):
        warnings.warn("Save method is obsolete and empty. Please delete all references from code.")

    @staticmethod
    def load(filename=None, strategy_context=None, directory=''):
        fn = filename

        if strategy_context is not None:
            smgr = Swarm(strategy_context)
            fn = os.path.join(directory, smgr.name+'.swm')

        with open(fn, 'rb') as f:
            return pickle.load(f)


    @property
    def last_date(self):
        """
        Last date of swarm calculation
        :return:
        """
        if self._last_date is None:
            raise ValueError("Run pick() method before access this property")
        return self._last_date

    @property
    def last_exposure(self):
        """
        Last net exposure of picked swarm
        :return:
        """
        if self._last_exposure is None:
            raise ValueError("Run pick() method before access this property")
        return self._last_exposure

    @property
    def last_prev_exposure(self):
        """
        Last net exposure of picked swarm
        :return:
        """
        if self._last_prev_exposure is None:
            raise ValueError("Run pick() method before access this property")
        return self._last_prev_exposure

    @property
    def last_exoquote(self):
        """
        Last EXO quote
        :return:
        """
        if self._last_exoquote is None:
            raise ValueError("Run pick() method before access this property")
        return self._last_exoquote

    @property
    def last_delta(self):
        """
        Last delta
        :return:
        """
        if self._last_delta is None:
            raise ValueError("Run pick() method before access this property")
        return self._last_delta

    @property
    def last_members_list(self):
        """
        Last member list for picked swarm
        :return:
        """
        if self._last_members_list is None:
            raise ValueError("Run pick() method before access this property")
        return self._last_members_list

    @property
    def last_rebalance_date(self):
        """
        Last rebalance date
        :return:
        """
        if self._last_rebalance_date is None:
            raise ValueError("Run pick() method before access this property")
        return self._last_rebalance_date

    def context_to_jsondict(self, context):
        if isinstance(context, dict):
            return {k: self.context_to_jsondict(v) for k, v in context.items()}
        elif isinstance(context, list):
            return [self.context_to_jsondict(elem) for elem in context]
        elif inspect.isclass(context):
            return context.__name__
        else:
            return str(context)  # no container, just values (str, int, float)

    def laststate_to_dict(self):
        """
        Return last state of swarm for online trading
        for MongoDB saving
        :return:
        """
        state_dict = {
            # Swarm structure info
            'last_date': self.last_date,
            'last_exposure': self.last_exposure,
            'last_prev_exposure': self.last_prev_exposure,
            'last_exoquote': self.last_exoquote,
            'last_members_list': self.last_members_list,
            'last_rebalance_date': self.last_rebalance_date,
            'last_delta': self.last_delta,
            'max_exposure': self.max_exposure,
            'swarm_series': pickle.dumps(self._swarm_series),
            # General info
            'swarm_name': self.name,
            'exo_name': self.exo_name,
            'alpha_name': self.strategy.name,
            'direction': self.direction[0],
            'instrument': self.instrument,
            'exo_type': self.exo_type,
            'calc_date': datetime.now(),
            # Context info
            'context_info': self.context_to_jsondict(self.context)
        }
        return state_dict

    @staticmethod
    def laststate_from_dict(state_dict, strategy_context):
        """
        Restores last swarm state from dictionary
        :return:
        """

        ctx = strategy_context
        ctx['strategy']['opt_preset'] = Swarm._parse_params(state_dict['last_members_list'])
        # Creating new swarm in special mode (used for online updates)
        swm = Swarm(ctx, laststate=True)

        swm._last_rebalance_date = state_dict['last_rebalance_date']
        swm._last_date = state_dict['last_date']
        swm._last_exposure = state_dict['last_exposure']
        swm._last_prev_exposure = state_dict['last_prev_exposure']
        swm._last_exoquote = state_dict['last_exoquote']
        swm._last_members_list = state_dict['last_members_list']
        swm._last_delta = state_dict['last_delta']
        swm._max_exposure = state_dict['max_exposure']
        swm._swarm_series = pickle.loads(state_dict['swarm_series'])

        return swm

    @property
    def max_exposure(self):
        """
        max(abs(picked_exposure)) of swarm
        :return:
        """
        if self._max_exposure is not None:
            # Return cached value if applicable
            return self._max_exposure

        self._max_exposure = self.picked_exposure.sum(axis=1).abs().max()
        return self._max_exposure


    def _laststate_update(self, exo_dataframe, swarm_exposure, costs=None):
        """
        Updates last equity, exposure, exo_quote (used for real time run)
        :param exo_dataframe: price series of EXO
        :param swarm_exposure: last net swarm exposure
        :param costs: EXO costs array
        :return: None
        """
        if self._swarm_series is None or len(self._swarm_series) <= 1:
            raise ValueError("Improperly initiated error: self._swarm_series is None "
                             "or len(self._equity) <= 1 ")

        if len(swarm_exposure) == 0:
            warnings.warn("Swarm ({0}) exposure is zero-length, seems that no members picked after rebalancing.".format(self.name))

        # 1. Filter exo_price and swarm_exposure >= self.last_date
        _exo_price_array = exo_dataframe['exo'][exo_dataframe.index >= self.last_date]
        _exo_delta_array = None
        if 'delta' in exo_dataframe:
            _exo_delta_array = exo_dataframe['delta'][exo_dataframe.index >= self.last_date]
        _swarm_exposure = swarm_exposure[swarm_exposure.index >= self.last_date]

        if len(_swarm_exposure) > 0 and len(_exo_price_array) != len(_swarm_exposure):
            raise ValueError("len(_swarm_exposure) > 0 and len(_exo_price_array) != len(_swarm_exposure)")


        for i in range(len(_exo_price_array)):
            # Do sanity checks
            # Check that date index matches
            _costs_value = 0.0
            delta_value = 0.0
            _exposure = 0.0

            if len(_swarm_exposure) > 0:
                if _exo_price_array.index[i] != _swarm_exposure.index[i]:
                    raise ValueError("_exo_price_array.index[i] != _swarm_exposure.index[i]")
                _exposure = _swarm_exposure.values[i]
            else:
                if self._last_date == _exo_price_array.index[i]:
                    _exposure = self.last_prev_exposure

            # We have new quote data
            # Similar to backtester_fast.stats_exposure() backtesting algorithm
            if i == 0:
                profit = (_exo_price_array.values[i] - self.last_exoquote) * self._last_prev_exposure
            else:
                profit = (_exo_price_array.values[i] - _exo_price_array.values[i-1]) * self._last_exposure
            if costs is not None:
                _costs_value = calc_costs(costs['transaction_costs'].values[i],
                                          costs['rollover_costs'].values[i],
                                          self.last_exposure,           # Prev Exposure
                                          _exposure)                    # Current Exposure
                profit += _costs_value

            # Updating swarm delta value if it exists in EXO dataframe

            if _exo_delta_array is not None:
                delta_value = _exo_delta_array.values[i] * _exposure


            # Use previous exposure to calculate quotes
            self._swarm_series.at[_exo_price_array.index[i], 'equity'] = self._swarm_series['equity'].values[-1] + profit
            self._swarm_series.at[_exo_price_array.index[i], 'delta'] = delta_value
            self._swarm_series.at[_exo_price_array.index[i], 'exposure'] = _exposure
            self._swarm_series.at[_exo_price_array.index[i], 'costs'] = _costs_value

            # Update self.last_* properties for next loop step
            if self._last_date != _exo_price_array.index[i]:
                #
                # Suppress last_exposure overwriting if we recalculating swarm on current date
                #
                self._last_prev_exposure = self._last_exposure
                self._last_exposure = _exposure
            self._last_exoquote = _exo_price_array.values[i]
            self._last_date = _exo_price_array.index[i]
            self._last_delta = delta_value

    def update(self):
        if not self._islast_state:
            raise Exception("update() method only applicable to swarms loaded from online last state dict")

        # Setting preset of swarm members to update
        self.context['strategy']['opt_preset'] = self._parse_params(self.last_members_list)

        # Run predefined swarm parameters
        self.run_swarm()

        # We are using self.raw_exposure instead of self.picked_exposure
        # because in self.update() we are running predefined (i.e. already picked) swarms
        # Update equity and another last state values
        self._laststate_update(self.strategy.data, self.raw_exposure.sum(axis=1), self.strategy.costs)

    @staticmethod
    def _parse_params(members_list):
        """
        Parse alpha-parameters tuple-string from MongoDB
        :param members_list: list of strings with stingified tuples params
        :return: list of tuples (params for alpha strategy)
        """
        return [literal_eval(p.strip()) for p in members_list]





