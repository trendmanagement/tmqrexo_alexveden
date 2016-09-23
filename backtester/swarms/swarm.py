import numpy as np
import pandas as pd
import pickle
import os
from ast import literal_eval
import pyximport; pyximport.install()
from backtester.backtester_fast import stats_exposure
from copy import  deepcopy
import inspect

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
        self._max_exposure = None

        self._equity = None

        self._islast_state = laststate

        strategy_settings = self.context['strategy']
        # Initialize strategy class
        self.strategy = strategy_settings['class'](self.context)



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
        if self._equity is None:
            raise ValueError("Run pick() method before access this property")
        return self._equity

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
            picked_swarm_equity[:, i], _stats_dict = stats_exposure(self.strategy.data['exo'], picked_swarm_exposure[:, i], self.strategy.costs)

        self._picked_swarm = pd.DataFrame(picked_swarm_equity, self._swarm.index)
        self._picked_inposition = pd.DataFrame(picked_swarm_inposition, self._swarm.index)
        self._picked_exposure = pd.DataFrame(picked_swarm_exposure, self._swarm.index)
        self.rebalance_info = rebalance_info

        # Storing last state values used in online calculations
        self.fill_last_state()

        # Apply separate backtesting engine func
        #  due to position netting in the swarm we will have different costs
        #  Also store Extended stats dictionary for swarms statistics
        self._equity, self._swarm_stats = stats_exposure(self.strategy.data['exo'], self.picked_exposure.sum(axis=1), self.strategy.costs, extendedstats=True)

    def fill_last_state(self):
        """
        Store last state values used in online calculations
        :return:
        """
        if len(self.picked_exposure) < 2 or len(self.rebalance_info) < 2:
            # Insufficient data
            return

        self._last_exposure = self.picked_exposure.iloc[-1].sum()
        self._last_prev_exposure = self.picked_exposure.iloc[-2].sum()
        self._last_date = self.picked_swarm.index[-1]
        self._last_members_list = self.rebalance_info[-1]['best_members']
        self._last_rebalance_date = self.rebalance_info[-1]['rebalance_date']
        self._last_exoquote = self.strategy.data['exo'].iloc[-1]


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
        direction_param = self.context['strategy']['opt_params'][0]

        if direction_param.name.lower() != 'direction':
            raise ValueError('First OptParam of strategy must be Direction')

        if len(direction_param.array) == 2:
            return 0,'Bidir'
        else:
            if direction_param.array[0] == 1:
                return 1, 'Long'
            elif direction_param.array[0] == -1:
                return -1, 'Short'

            raise ValueError("Unexpected direction parameter value")

    @property
    def name(self):
        """
        Return swarm manager human-readable name
        Underlying_EXOName_Strategy_Direction
        :return:
        """
        exoname = self.strategy.exoinfo.exo_info['name']
        strategyname = self.strategy.name

        suffix = ''
        if 'suffix' in self.context['strategy'] \
                and self.context['strategy']['suffix'] is not None \
                and len(self.context['strategy']['suffix']) > 0:
            suffix = "_" + self.context['strategy']['suffix']

        return '{0}_{1}_{2}{3}'.format(exoname, self.direction[1], strategyname, suffix)

    def save(self, directory,  filename=None):
        if not os.path.isdir(directory):
            os.makedirs(directory)

        if filename is None:
            fn = os.path.join(directory, self.name + '.swm')
        else:
            fn = filename

        with open(fn, 'wb') as f:
            pickle.dump(self, f)

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
            'max_exposure': self.max_exposure,
            'picked_equity': pickle.dumps(self.picked_equity),
            # General info
            'swarm_name': self.name,
            'exo_name': self.exo_name,
            'alpha_name': self.strategy.name,
            'direction': self.direction[0],
            'instrument': self.instrument,
            'exo_type': self.exo_type,
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
        swm._max_exposure = state_dict['max_exposure']
        swm._equity = pickle.loads(state_dict['picked_equity'])

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

        if self._picked_exposure is None:
            raise ValueError("Run pick() method before access this property")

        self._max_exposure = self.picked_exposure.sum(axis=1).abs().max()
        return self._max_exposure


    def laststate_update(self, exo_price, swarm_exposure, costs=None):
        """
        Updates last equity, exposure, exo_quote (used for real time run)
        :param exo_price: price series of EXO
        :param swarm_exposure: last net swarm exposure
        :param costs: EXO costs array
        :return: None
        """
        if self._equity is None or len(self._equity) <= 1:
            raise ValueError("Improperly initiated error: self._equity is None or len(self._equity) <= 1")


        # 1. Filter exo_price and swarm_exposure >= self.last_date
        _exo_price = exo_price[exo_price.index >= self.last_date]
        _swarm_exposure = swarm_exposure[swarm_exposure.index >= self.last_date]

        if len(_exo_price) != len(_swarm_exposure):
            raise ValueError("len(_exo_price) != len(_swarm_exposure)")


        for i in range(len(_exo_price)):
            # Do sanity checks
            # Check that date index matches
            if _exo_price.index[i] != _swarm_exposure.index[i]:
                raise ValueError("len(_exo_price) != len(_swarm_exposure)")

            # Check that exo_quote is matching in history
            # To avoid calculation mistakes
            if _exo_price.index[i] == self.last_date:
                if _exo_price.values[i] != self.last_exoquote:
                    raise ValueError("New historical EXO price doesn't match the last_exoquote on same day! Is EXO recalculated?")

                # Just ignore same date swarm updates
            else: # Date of EXO price > self.last_date

                # We have new quote data
                # Update equity series with (exo_price[i] - self.last_exoquote) * self.last_exposure

                # Similar to backtester_fast.stats_exposure() backtesting algorithm
                profit = (_exo_price.values[i] - self.last_exoquote) * self.last_exposure
                if costs is not None and self.last_exposure != _swarm_exposure.values[i]:
                    _costs_value = (-abs(costs[i]) * abs(self.last_exposure - _swarm_exposure.values[i]))
                    profit += _costs_value
                    # TODO: store costs_value into costs array


                # Use previous exposure to calculate quotes
                self._equity[_exo_price.index[i]] = self._equity.values[-1] + profit

                # Update self.last_* properties for next loop step
                self._last_exoquote = _exo_price.values[i]
                self._last_date = _exo_price.index[i]
                self._last_prev_exposure = self._last_exposure
                self._last_exposure = _swarm_exposure.values[i]

    def update(self):
        if not self._islast_state:
            raise Exception("update() method only applicable to swarms loaded from online last state dict")

        # Run predefined swarm parameters
        self.run_swarm()

        if len(self.raw_exposure) > 0:
            # Update equity and another last state values
            self.laststate_update(self.strategy.data['exo'], self.raw_exposure.sum(axis=1))
        else:
            # TODO: decide if it is unexpected case when no systems picked in some reasons?
            pass

    @staticmethod
    def _parse_params(members_list):
        """
        Parse alpha-parameters tuple-string from MongoDB
        :param members_list: list of strings with stingified tuples params
        :return: list of tuples (params for alpha strategy)
        """
        return [literal_eval(p.strip()) for p in members_list]





