import unittest
import pandas as pd
import numpy as np

from backtester.swarms.swarm import Swarm

from backtester.strategy import StrategyBase, OptParam, OptParamArray
from backtester.swarms.ranking import SwarmRanker
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.filters import SwarmFilter
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import *

from strategies.strategy_macross_with_trail import StrategyMACrossTrail

from copy import deepcopy
import pyximport; pyximport.install()
from backtester.backtester_fast import stats_exposure
from unittest.mock import Mock, patch


class BacktesterTestCase(unittest.TestCase):
    def reblance_every_5th(self, swarm):
        return pd.Series(swarm.index % 5 == 0, index=swarm.index)

    def setUp(self):
        self.STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': './mat/strategy_270225.mat',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 1,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': self.reblance_every_5th
            }
        }

    def test_pick_equity_calculation(self):


        def reblance_every_5th(swarm):
            return pd.Series(swarm.index % 5 == 0, index=swarm.index)

        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': './strategy_270225.mat',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 1,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': reblance_every_5th
            }
        }
        swm_index = np.array(range(20))
        swm_values = np.array([
           [ 0.,  0.], # 0
           [ 1.,  -1.],
           [ 2.,  -2.],
           [ 3.,  -3.],
           [ 4.,  -4.],
           [ 5.,  -5.], # 5
           [ 6.,  -6.],
           [ 7.,  -7.],
           [ 8.,  -8.],
           [ 9.,  -9.],
           [ 6.,  -6.], # 10
           [ 5.,  -5.],
           [ 4.,  -4.],
           [ 3.,  -3.],
           [ 2.,  -2.],
           [ 1.,  -1.],   #15
           [ 0.,  0.],
           [ -1.,  1.],
           [ -2.,  2.],
           [ -3.,  3.]])

        exo_price = np.array([
            0,
            1,
            2,
            3,
            4,
            5,  # 5
            6,
            7,
            8,
            9,
            6,  # 10
            5,
            4,
            3,
            2,
            1,
            0,
            -1,
            -2,
            -3
        ])
        exposure_values = np.array([
            [1., -1.],  # 0
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],  # 5
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],  # 10
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],
        ])

        swm = Swarm(STRATEGY_CONTEXT)
        swm._swarm = pd.DataFrame(swm_values, swm_index)
        swm._swarm_inposition = pd.DataFrame(np.ones((20, 2)), swm_index)
        swm._swarm_exposure = pd.DataFrame(exposure_values, swm_index, dtype=np.float)
        swm.strategy.data = pd.DataFrame({'exo': pd.Series(exo_price, index=swm_index, dtype=np.float)})
        swm.strategy.costs = None

        swm_res = np.array([
           [ 0.], #0 - ignored by default
           [ 0.],
           [ 0.],
           [ 0.],
           [ 0.],
           [ 0.], #5 - first rebalance (pick system #0)
           [ 0.], # Apply delayed rebalance we checked rebalance on #5 but change the position at #6
           [ 1.],
           [ 2.],
           [ 3.],
           [ 0.], #10 - pick another systems (but keep prev system change to next day)
           [ -1.], # Apply delayed rebalance we checked rebalance on #10 but change the position at #11
           [ 0.],
           [ 1.],
           [ 2.],
           [ 3.], #15 - keep system #1
           [ 4.],
           [ 5.],
           [ 6.],
           [ 7.]] )

        expected = pd.DataFrame(swm_res, index=swm_index)

        swm.pick()

        for k, v in expected[0].items():
            print(k)
            self.assertEqual(k, swm.picked_swarm.index[k])
            self.assertEqual(v, swm.picked_swarm[0][k])

    def test_rebalanceinformation_before_next_day(self):

        def riseup(swarm_slice, nsystems):
            result = []
            rank_info = []

            # Calculate 14-period equity returns and sort values
            last_diff = swarm_slice.diff(periods=1).iloc[-1, :].sort_values(ascending=False)

            # Pick best nsystems
            best = last_diff[:nsystems]

            for k, v in best.items():
                if not np.isnan(v) and v > 0:
                    result.append(k)
                    rank_info.append({'rank_value': v})

            return result, rank_info

        def reblance_every_5th(swarm):
            return pd.Series(swarm.index % 5 == 0, index=swarm.index)

        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': 'strategy_270225',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 1,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': reblance_every_5th
            }
        }
        swm_index = np.array(range(11))
        swm_values = np.array([
           [ 0.,  0.], # 0
           [ 1.,  -1.],
           [ 2.,  -2.],
           [ 3.,  -3.],
           [ 4.,  -4.],
           [ 5.,  -5.], # 5
           [ 6.,  -6.],
           [ 7.,  -7.],
           [ 8.,  -8.],
           [ 9.,  -9.],
           [ 6.,  -6.], # 10
           ])

        exposure_values = np.array([
            [1., -1.],  # 0
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],  # 5
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],  # 10
        ])

        exo_price = np.array([
            0,
            1,
            2,
            3,
            4,
            5,   # 5
            6,
            7,
            8,
            9,
            6    #10
        ])

        swm = Swarm(STRATEGY_CONTEXT)
        swm._swarm = pd.DataFrame(swm_values, swm_index)
        swm._swarm_inposition = pd.DataFrame(np.ones((11, 2)), swm_index)
        swm._swarm_exposure = pd.DataFrame(exposure_values, swm_index, dtype=np.float)
        swm.strategy.data = pd.DataFrame({'exo': pd.Series(exo_price, index=swm_index, dtype=np.float)})
        swm.strategy.costs = None

        #equity1, _st_pass = stats_exposure(swm.strategy.data['exo'], swm._swarm_exposure[1], costs=None)



        swm_res = np.array([
           [ 0.], #0 - ignored by default
           [ 0.],
           [ 0.],
           [ 0.],
           [ 0.],
           [ 0.], #5 - first rebalance (pick system #0)
           [ 0.], # Apply delayed rebalance we checked rebalance on #5 but change the position at #6
           [ 1.],
           [ 2.],
           [ 3.],
           [ 0.], #10 - pick another systems (but keep prev system change to next day)
        ])

        expected = pd.DataFrame(swm_res, index=swm_index)

        swm.pick()

        self.assertEqual(2, len(swm.rebalance_info))
        self.assertEqual(5, swm.rebalance_info[0]['rebalance_date'])
        self.assertEqual(10, swm.rebalance_info[1]['rebalance_date'])

        for k, v in expected[0].items():
            print(k)
            self.assertEqual(k, swm.picked_swarm.index[k])
            self.assertEqual(v, swm.picked_swarm[0][k])

    def test_laststate_update(self):


        def reblance_every_5th(swarm):
            return pd.Series(swarm.index % 5 == 0, index=swarm.index)

        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': './mat/strategy_270225.mat',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 1,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': reblance_every_5th
            }
        }
        swm_index = np.array(range(11))
        swm_values = np.array([
           [ 0.,  0.], # 0
           [ 1.,  -1.],
           [ 2.,  -2.],
           [ 3.,  -3.],
           [ 4.,  -4.],
           [ 5.,  -5.], # 5
           [ 6.,  -6.],
           [ 7.,  -7.],
           [ 8.,  -8.],
           [ 9.,  -9.],
           [ 6.,  -6.], # 10
           ])

        exo_price = np.array([
            0,
            1,
            2,
            3,
            4,
            5,  # 5
            6,
            7,
            8,
            9,
            6  # 10
        ])
        exposure_values = np.array([
            [1., -1.],  # 0
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],  # 5
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],
            [1., -1.],  # 10
        ])

        swm = Swarm(STRATEGY_CONTEXT)
        swm._swarm = pd.DataFrame(swm_values, swm_index)
        swm._swarm_inposition = pd.DataFrame(np.ones((11, 2)), swm_index)
        swm._swarm_exposure = pd.DataFrame(exposure_values, swm_index, dtype=np.float)
        swm.strategy.data = pd.DataFrame({'exo': pd.Series(exo_price, index=swm_index, dtype=np.float)})
        swm.strategy.costs = None

        swm_res = np.array([
            0., #0 - ignored by default
            0.,
            0.,
            0.,
            0.,
            0., #5 - first rebalance (pick system #0)
            0., # Apply delayed rebalance we checked rebalance on #5 but change the position at #6
            1.,
            2.,
            3.,
            0., #10 - pick another systems (but keep prev system change to next day)
        ])

        expected = pd.DataFrame(swm_res, index=swm_index)

        swm.pick()

        self.assertEqual(2, len(swm.rebalance_info))
        self.assertEqual(5, swm.rebalance_info[0]['rebalance_date'])
        self.assertEqual(10, swm.rebalance_info[1]['rebalance_date'])

        for k, v in expected[0].items():
            #print(k)
            self.assertEqual(k, swm.picked_swarm.index[k])
            self.assertEqual(v, swm.picked_swarm[0][k])

        self.assertEqual(swm.last_date, 10)
        self.assertEqual(swm.last_rebalance_date, 10)
        self.assertEqual(swm.last_exposure, 1)
        self.assertEqual(swm.last_members_list, [1])
        self.assertEqual(True, np.all(swm.picked_equity.values == expected[0].values))


        #
        #  DO swarm update with new quotes
        #
        swm_index = np.array(range(14))


        exo_price = np.array([
            0.,  # 0 - ignored by default
            0.,
            0.,
            0.,
            0.,
            0.,  # 5 - first rebalance (pick system #0)
            0.,  # Apply delayed rebalance we checked rebalance on #5 but change the position at #6
            1.,
            2.,
            3.,
            0.,  # 10 - pick another systems (but keep prev system change to next day)
            10., # Should be added with last exposure
            11.,
            13.
        ])

        swarm_exposure = np.array([
            0.,  # 0 - ignored by default
            0.,
            0.,
            0.,
            0.,
            0.,  # 5 - first rebalance (pick system #0)
            0.,
            0.,
            0.,
            0.,
            0.,  # 10
            2.,  # Should be added with last exposure
            2.,
            2.,
        ])

        #swm = Swarm(STRATEGY_CONTEXT)
        # Little hack
        swm._last_exoquote = 0.0 # exo_price on #10
        # Little hack
        swm._last_exposure = -1
        self.assertEqual(swm.last_date, 10)
        self.assertEqual(swm.last_rebalance_date, 10)
        self.assertEqual(swm.last_exposure, -1)
        self.assertEqual(swm.last_exoquote, 0)
        self.assertEqual(swm.last_members_list, [1])

        exo_df = pd.DataFrame({'exo': exo_price}, index=swm_index)

        swm._laststate_update(exo_df, pd.Series(swarm_exposure, index=swm_index))

        self.assertEqual(swm.last_date, 13)
        self.assertEqual(swm.last_rebalance_date, 10)
        self.assertEqual(swm.last_exposure, 2)
        self.assertEqual(swm.last_exoquote, 13)
        self.assertEqual(swm.last_members_list, [1])

        swm_res = np.array([
            0.,  # 0 - ignored by default
            0.,
            0.,
            0.,
            0.,
            0.,  # 5 - first rebalance (pick system #0)
            0.,  # Apply delayed rebalance we checked rebalance on #5 but change the position at #6
            1.,
            2.,
            3.,
            0.,  # 10 - pick another systems (but keep prev system change to next day)
            -10.,  # Apply delayed rebalance we checked rebalance on #10 but change the position at #11
            -8.,
            -4.,
            ])
        expected = pd.Series(swm_res, index=swm_index)

        self.assertEqual(len(swm.picked_equity), len(expected))
        for k, v in expected.items():
            print(k)
            self.assertEqual(k, swm.picked_equity.index[k])
            self.assertEqual(v, swm.picked_equity.values[k])

    def test_laststate_update_real(self):
        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': './mat/strategy_270225.mat',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 3,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': SwarmRebalance.every_friday
            }
        }

        swm_full = Swarm(STRATEGY_CONTEXT)
        swm_full.run_swarm()
        swm_full.pick()


        swm_start = Swarm(STRATEGY_CONTEXT)
        swm_start.strategy.data = swm_start.strategy.data.ix[:'2016-03-04']
        swm_start.run_swarm()
        swm_start.pick()

        ctx = deepcopy(STRATEGY_CONTEXT)
        ctx['strategy']['opt_preset'] = Swarm._parse_params(swm_start.last_members_list)
        swm_next = Swarm(ctx)
        swm_next.strategy.data = swm_next.strategy.data.ix[:'2016-03-11']
        swm_next.run_swarm()

        self.assertEqual(swm_full.picked_equity.ix['2016-03-04'], swm_start.picked_equity.ix['2016-03-04'])

        self.assertEqual(-2, swm_start.last_exposure)

        # Updating swm_start (assuming that it was loaded from DB)
        swm_start._laststate_update(swm_next.strategy.data, swm_next.raw_exposure.sum(axis=1))

        self.assertEqual(swm_full.picked_equity.ix['2016-03-04'], swm_start.picked_equity.ix['2016-03-04'])

        self.assertAlmostEqual(swm_full.picked_equity.ix['2016-03-07'], swm_start.picked_equity.ix['2016-03-07'])

        self.assertAlmostEqual(swm_full.picked_equity.ix['2016-03-10'], swm_start.picked_equity.ix['2016-03-10'])

        self.assertAlmostEqual(swm_full.picked_equity.ix['2016-03-11'], swm_start.picked_equity.ix['2016-03-11'])

        self.assertEqual(-3, swm_start.last_exposure)

    @patch('backtester.costs.CostsManagerEXOFixed.get_costs')
    def test_laststate_update_real_with_costs(self, mock_get_costs):
        from backtester.matlab import loaddata

        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': './mat/strategy_270225.mat',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 3,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': SwarmRebalance.every_friday
            },
            'costs': {
                'manager': CostsManagerEXOFixed,
                'context': {
                    'costs_options': 3.0,
                    'costs_futures': 3.0,
                }
            }
        }
        #
        # Mocking the CostsManagerEXOFixed.get_costs
        #
        exo_df, info = loaddata('./mat/strategy_270225.mat')
        mock_get_costs.return_value = pd.DataFrame({'rollover_costs': np.zeros(len(exo_df.index)),
                                                    'transaction_costs': np.ones(len(exo_df.index)) * 10}, index=exo_df.index)

        swm_full = Swarm(STRATEGY_CONTEXT)
        swm_full.strategy.data.loc[:, 'delta'] = 1.0
        swm_full.run_swarm()
        swm_full.pick()


        swm_start = Swarm(STRATEGY_CONTEXT)
        swm_start.strategy.data = swm_start.strategy.data.ix[:'2016-03-18']
        swm_start.strategy.data.loc[:, 'delta'] = 1.0
        swm_start.run_swarm()
        swm_start.pick()

        ctx = deepcopy(STRATEGY_CONTEXT)
        ctx['strategy']['opt_preset'] = Swarm._parse_params(swm_start.last_members_list)
        swm_next = Swarm(ctx)
        swm_next.strategy.data = swm_next.strategy.data.ix[:'2016-03-25']
        swm_next.strategy.data.loc[:, 'delta'] = 1.0
        swm_next.run_swarm()

        dt = '2016-03-18'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(np.isnan(swm_full.series['delta'].ix[dt]), np.isnan(swm_start.series['delta'].ix[dt]))

        self.assertEqual(swm_start.last_exposure, swm_full.picked_exposure.sum(axis=1).ix['2016-03-18'])


        # Updating swm_start (assuming that it was loaded from DB)
        swm_start._laststate_update(swm_next.strategy.data, swm_next.raw_exposure.sum(axis=1), swm_next.strategy.costs)

        dt = '2016-03-21'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-22'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-23'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-24'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-25'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

    def test_laststate_update_recalculated_exo_price(self):
        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': './mat/strategy_270225.mat',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 3,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': SwarmRebalance.every_friday
            },
        }

        swm_full = Swarm(STRATEGY_CONTEXT)
        swm_full.run_swarm()
        swm_full.pick()

        swm_start = Swarm(STRATEGY_CONTEXT)
        swm_start.strategy.data.at[pd.Timestamp('2016-03-04'), 'exo'] += 10

        swm_start.strategy.data = swm_start.strategy.data.ix[:'2016-03-04']
        swm_start.run_swarm()
        swm_start.pick()

        ctx = deepcopy(STRATEGY_CONTEXT)
        ctx['strategy']['opt_preset'] = Swarm._parse_params(swm_start.last_members_list)
        swm_next = Swarm(ctx)
        swm_next.strategy.data = swm_next.strategy.data.ix[:'2016-03-11']
        swm_next.run_swarm()

        # Make sure that old EXO price used
        self.assertEqual(-2, swm_start.last_exposure)
        self.assertEqual(swm_full.picked_equity.ix['2016-03-04'], swm_start.picked_equity.ix['2016-03-04'] - 10*swm_start.last_exposure)



        # After this run
        swm_start._laststate_update(swm_next.strategy.data, swm_next.raw_exposure.sum(axis=1))

        self.assertEqual(swm_full.picked_equity.ix['2016-03-04'], swm_start.picked_equity.ix['2016-03-04'])

        self.assertAlmostEqual(swm_full.picked_equity.ix['2016-03-07'], swm_start.picked_equity.ix['2016-03-07'])

        self.assertAlmostEqual(swm_full.picked_equity.ix['2016-03-10'], swm_start.picked_equity.ix['2016-03-10'])

        self.assertAlmostEqual(swm_full.picked_equity.ix['2016-03-11'], swm_start.picked_equity.ix['2016-03-11'])

        self.assertEqual(-3, swm_start.last_exposure)

    def test_laststate_update_handle_if_swarm_composition_is_empty_after_rebalance(self):
        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': './mat/strategy_270225.mat',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 3,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': SwarmRebalance.every_friday
            },
        }

        swm_full = Swarm(STRATEGY_CONTEXT)
        swm_full.strategy.data.at[pd.Timestamp('2016-03-04'), 'exo'] = swm_full.strategy.data.ix['2016-03-03']['exo']
        swm_full.run_swarm()
        swm_full.pick()

        swm_start = Swarm(STRATEGY_CONTEXT)
        swm_start.strategy.data.at[pd.Timestamp('2016-03-04'), 'exo'] = swm_full.strategy.data.ix['2016-03-03']['exo']

        swm_start.strategy.data = swm_start.strategy.data.ix[:'2016-03-04']
        swm_start.run_swarm()
        swm_start.pick()

        ctx = deepcopy(STRATEGY_CONTEXT)
        ctx['strategy']['opt_preset'] = Swarm._parse_params(swm_start.last_members_list)

        swm_next = Swarm(ctx)
        swm_next.strategy.data.at[pd.Timestamp('2016-03-04'), 'exo'] = swm_full.strategy.data.ix['2016-03-03']['exo']
        swm_next.strategy.data = swm_next.strategy.data.ix[:'2016-03-11']
        swm_next.run_swarm()

        # Make sure that old EXO price used
        self.assertEqual(-2, swm_start.last_exposure)
        self.assertEqual(swm_full.picked_equity.ix['2016-03-03'], swm_start.picked_equity.ix['2016-03-04'])


        # After this run
        with patch('warnings.warn') as mock_warn:
            swm_start._laststate_update(swm_next.strategy.data, swm_next.raw_exposure.sum(axis=1))
            self.assertTrue(mock_warn.called)

        dt = '2016-03-04'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-07'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-08'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-09'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-10'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-11'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

    @patch('backtester.costs.CostsManagerEXOFixed.get_costs')
    def test_laststate_update_handle_if_swarm_composition_is_empty_after_rebalance_with_costs(self, mock_get_costs):
        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': './mat/strategy_270225.mat',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 3,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': SwarmRebalance.every_friday
            },
        }
        #
        # Mocking the CostsManagerEXOFixed.get_costs
        #
        from backtester.matlab import loaddata
        exo_df, info = loaddata('./mat/strategy_270225.mat')
        mock_get_costs.return_value = pd.DataFrame({'rollover_costs': np.zeros(len(exo_df.index)),
                                                    'transaction_costs': np.ones(len(exo_df.index)) * 10},
                                                   index=exo_df.index)


        swm_full = Swarm(STRATEGY_CONTEXT)
        swm_full.strategy.data.at[pd.Timestamp('2016-03-04'), 'exo'] = swm_full.strategy.data.ix['2016-03-03']['exo']
        swm_full.strategy.data.loc[:, 'delta'] = 1.0
        swm_full.run_swarm()
        swm_full.pick()

        swm_start = Swarm(STRATEGY_CONTEXT)
        swm_start.strategy.data.at[pd.Timestamp('2016-03-04'), 'exo'] = swm_full.strategy.data.ix['2016-03-03']['exo']

        swm_start.strategy.data = swm_start.strategy.data.ix[:'2016-03-04']
        swm_start.strategy.data.loc[:, 'delta'] = 1.0

        swm_start.run_swarm()
        swm_start.pick()

        ctx = deepcopy(STRATEGY_CONTEXT)
        ctx['strategy']['opt_preset'] = Swarm._parse_params(swm_start.last_members_list)

        swm_next = Swarm(ctx)
        swm_next.strategy.data.at[pd.Timestamp('2016-03-04'), 'exo'] = swm_full.strategy.data.ix['2016-03-03']['exo']
        swm_next.strategy.data = swm_next.strategy.data.ix[:'2016-03-11']
        swm_next.strategy.data.loc[:, 'delta'] = 1.0
        swm_next.run_swarm()

        # Make sure that old EXO price used
        self.assertEqual(-2, swm_start.last_exposure)
        self.assertEqual(swm_full.picked_equity.ix['2016-03-03'], swm_start.picked_equity.ix['2016-03-04'])


        # After this run
        with patch('warnings.warn') as mock_warn:
            swm_start._laststate_update(swm_next.strategy.data, swm_next.raw_exposure.sum(axis=1), swm_next.strategy.costs)
            self.assertTrue(mock_warn.called)

        dt = '2016-03-04'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-07'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-08'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-09'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-10'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

        dt = '2016-03-11'
        self.assertEqual(swm_full.series['equity'].ix[dt], swm_start.series['equity'].ix[dt])
        self.assertEqual(swm_full.series['exposure'].ix[dt], swm_start.series['exposure'].ix[dt])
        self.assertEqual(swm_full.series['costs'].ix[dt], swm_start.series['costs'].ix[dt])
        self.assertEqual(swm_full.series['delta'].ix[dt], swm_start.series['delta'].ix[dt])

    def test_laststate_save_load(self):
        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': './strategy_270225.mat',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 3,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': SwarmRebalance.every_friday
            }
        }

        swm = Swarm(STRATEGY_CONTEXT)
        swm.run_swarm()
        swm.pick()

        self.assertEqual(False, swm._islast_state)

        s = swm.laststate_to_dict()
        import pickle

        self.assertEqual(s['direction'], -1)
        self.assertEqual(s['alpha_name'], StrategyMACrossTrail.name)
        self.assertEqual(s['exo_name'], swm.exo_name )
        self.assertEqual(s['swarm_name'], swm.name )
        self.assertEqual(s['swarm_series'],  pickle.dumps(swm._swarm_series))
        self.assertEqual(s['last_rebalance_date'], swm.last_rebalance_date)
        self.assertEqual(s['last_members_list'], swm.last_members_list)
        self.assertEqual(s['last_exoquote'], swm.last_exoquote )
        self.assertEqual(s['last_prev_exposure'], swm.last_prev_exposure)
        self.assertEqual(s['last_exposure'], swm.last_exposure)
        self.assertEqual(s['last_date'], swm.last_date)
        self.assertEqual(s['instrument'], swm.instrument)
        self.assertEqual(s['exo_type'], swm.exo_type)
        self.assertEqual(s['max_exposure'], swm.max_exposure)


        swm = Swarm.laststate_from_dict(s, STRATEGY_CONTEXT)
        self.assertEqual(True, swm._islast_state)

        self.assertEqual(swm.direction[0], -1)
        self.assertEqual(swm.strategy.name, StrategyMACrossTrail.name)
        self.assertEqual(s['exo_name'], swm.exo_name)
        self.assertEqual(s['swarm_name'], swm.name)
        self.assertEqual(s['last_rebalance_date'], swm.last_rebalance_date)
        self.assertEqual(s['last_members_list'], swm.last_members_list)
        self.assertEqual(s['last_exoquote'], swm.last_exoquote)
        self.assertEqual(s['last_prev_exposure'], swm.last_prev_exposure)
        self.assertEqual(s['last_exposure'], swm.last_exposure)
        self.assertEqual(s['last_date'], swm.last_date)
        self.assertEqual(s['instrument'], swm.instrument)
        self.assertEqual(s['exo_type'], swm.exo_type)
        self.assertEqual(s['max_exposure'], swm.max_exposure)

        eq = pickle.loads(s['swarm_series'])['equity']

        self.assertEqual(True, np.all(eq == swm.picked_equity.values))

    def test_laststate_update_real_high_level(self):
        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': './strategy_270225.mat',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 3,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': SwarmRebalance.every_friday
            }
        }


        swm_start = Swarm(STRATEGY_CONTEXT)
        swm_start.strategy.data = swm_start.strategy.data.ix[:'2016-03-04']
        swm_start.run_swarm()
        swm_start.pick()

        self.assertEqual(19165.0, swm_start.picked_equity.ix['2016-03-04'])
        self.assertEqual(-2, swm_start.last_exposure)


        swarm_dict = swm_start.laststate_to_dict()
        # Loading and updating swarm online
        swm_start = Swarm.laststate_from_dict(swarm_dict, STRATEGY_CONTEXT)
        swm_start.update()


        self.assertEqual(19165.0, swm_start.picked_equity.ix['2016-03-04'])

        self.assertAlmostEqual(19335.0, swm_start.picked_equity.ix['2016-03-07'])

        self.assertAlmostEqual(18990.0, swm_start.picked_equity.ix['2016-03-10'])

        self.assertAlmostEqual(20235.0, swm_start.picked_equity.ix['2016-03-11'])

    def test_laststate_update_different_lengths(self):
        exo_data = pd.DataFrame({
            'exo': [1, 2, 3, 4, 5]

        }, index=[1, 2, 3, 4, 5])

        swarm_exposure = pd.Series(
            [1, 2, 3, 4],
            index=[1, 2, 3, 4]
        )
        swm = Swarm(self.STRATEGY_CONTEXT)
        swm._swarm_series = None
        self.assertRaises(ValueError, swm._laststate_update, exo_data, None)

        swm._swarm_series = [0]
        self.assertRaises(ValueError, swm._laststate_update, exo_data, None)

        swm._swarm_series = [0, 2]
        self.assertRaises(ValueError, swm._laststate_update, exo_data, swarm_exposure)

    def test_laststate_update_different_lengths_after_last_date(self):
        exo_data = pd.DataFrame({
            'exo': [1, 2, 3, 4, 5]

        }, index=[1, 2, 3, 4, 5])

        swarm_exposure = pd.Series(
            [1, 2, 3, 5, 6],
            index=[1, 2, 3, 5, 6]
        )
        swm = Swarm(self.STRATEGY_CONTEXT)
        swm._last_date = 5
        # Mocking
        swm._swarm_series = swarm_exposure
        self.assertRaises(ValueError, swm._laststate_update, exo_data, swarm_exposure)

    def test_laststate_update_different_indexes_last_date(self):
        exo_data = pd.DataFrame({
            'exo': [1, 2, 3, 5, 6]

        }, index=[1, 2, 3, 6, 7])

        swarm_exposure = pd.Series(
            [1, 2, 3, 5, 6],
            index=[1, 2, 3, 5, 7]
        )
        swm = Swarm(self.STRATEGY_CONTEXT)
        swm._last_date = 5
        # Mocking
        swm._swarm_series = swarm_exposure
        self.assertRaises(ValueError, swm._laststate_update, exo_data, swarm_exposure)

    def test_raw_equity(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.raw_equity
        self.assertRaises(ValueError, property_raises, self)

    def test_raw_swarm(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.raw_swarm
        self.assertRaises(ValueError, property_raises, self)

    def test_raw_inposition(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.raw_inposition
        self.assertRaises(ValueError, property_raises, self)

    def test_raw_exposure(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.raw_exposure
        self.assertRaises(ValueError, property_raises, self)

    def test_picked_swarm(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.picked_swarm
        self.assertRaises(ValueError, property_raises, self)

    def test_picked_inposition(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.picked_inposition
        self.assertRaises(ValueError, property_raises, self)

    def test_picked_exposure(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.picked_exposure
        self.assertRaises(ValueError, property_raises, self)

    def test_picked_equity(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.picked_equity
        self.assertRaises(ValueError, property_raises, self)

    def test_picked_stats(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.picked_stats
        self.assertRaises(ValueError, property_raises, self)

    def test_picked_delta(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.picked_delta
        self.assertRaises(ValueError, property_raises, self)

    def test_series(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.series
        self.assertRaises(ValueError, property_raises, self)

    def test_rebalancetime(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.rebalancetime
        self.assertRaises(ValueError, property_raises, self)

    def test_last_date(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.last_date
        self.assertRaises(ValueError, property_raises, self)

    def test_last_exposure(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.last_exposure
        self.assertRaises(ValueError, property_raises, self)

    def test_last_prev_exposure(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.last_prev_exposure
        self.assertRaises(ValueError, property_raises, self)

    def test_last_exoquote(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.last_exoquote
        self.assertRaises(ValueError, property_raises, self)

    def test_last_delta(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.last_delta
        self.assertRaises(ValueError, property_raises, self)

    def test_last_members_list(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.last_members_list
        self.assertRaises(ValueError, property_raises, self)

    def test_last_rebalance_date(self):
        def property_raises(self):
            swm = Swarm(self.STRATEGY_CONTEXT)
            swm.last_rebalance_date
        self.assertRaises(ValueError, property_raises, self)

    def test_get_direction(self):
        ctx = {
            'strategy': {
                'direction': -1,
                'opt_params': [
                    OptParamArray('Direction', [-1]),
                ],
            },
        }
        with patch('warnings.warn') as mock_warn:
            Swarm.get_direction(ctx)
            self.assertTrue(mock_warn.called)

        ctx = {
            'strategy': {
                'opt_params': [
                    OptParamArray('Direction', [-1]),
                ],
            },
        }
        self.assertEqual((-1, 'Short'), Swarm.get_direction(ctx))

        ctx = {
            'strategy': {
                'opt_params': [
                    OptParamArray('Direction', [1]),
                ],
            },
        }
        self.assertEqual((1, 'Long'), Swarm.get_direction(ctx))

        ctx = {
            'strategy': {
                'opt_params': [
                    OptParamArray('Direction', [1, -1]),
                ],
            },
        }
        self.assertEqual((0, 'Bidir'), Swarm.get_direction(ctx))

        ctx = {
            'strategy': {
                'opt_params': [
                    OptParamArray('AnotherOptParam', [1, -1]),
                ],
            },
        }
        self.assertRaises(ValueError, Swarm.get_direction, ctx)

        ctx = {
            'strategy': {
                'opt_params': [
                    OptParamArray('Direction', [1, -1, 1]),
                ],
            },
        }
        self.assertRaises(ValueError, Swarm.get_direction, ctx)

        ctx = {
            'strategy': {
                'opt_params': [
                    OptParamArray('Direction', [2]),
                ],
            },
        }
        self.assertRaises(ValueError, Swarm.get_direction, ctx)

