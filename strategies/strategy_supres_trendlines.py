from backtester.analysis import *
from backtester.strategy import StrategyBase
import pandas as pd
import numpy as np


class Strategy_SupRes_TrendLines(StrategyBase):
    name = 'Strategy_SupRes_TrendLines'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    def calc_trendlines(self, px_ser, rolling_window_period):
        tl_df = pd.DataFrame(px_ser.values, columns=['px_ser'], index=px_ser.index)

        rollingmax = tl_df.px_ser.rolling(rolling_window_period).max()
        rollingmin = tl_df.px_ser.rolling(rolling_window_period).min()

        tl_df['highs'] = (rollingmax != tl_df.px_ser) & (rollingmax.shift(1) == tl_df.px_ser.shift(1))

        tl_df['lows'] = (rollingmin != tl_df.px_ser) & (rollingmin.shift(1) == tl_df.px_ser.shift(1))

        tl_df.loc[tl_df.lows == True, 'lows_price'] = rollingmin.shift(1)
        tl_df.loc[tl_df.highs == True, 'highs_price'] = rollingmax.shift(1)

        lows = tl_df[tl_df.lows == True]



        sup_tl_n = 0

        for i in lows.index:
            if i != lows.index[0]:
                lows_diff_w_current_low = (lows.lows_price.ix[i] - lows.ix[:i].lows_price).abs().sort_values()
                sup_line_col = 'sup_tl_' + str(sup_tl_n)

                tl_df[sup_line_col] = np.NaN

                tl_df.loc[lows_diff_w_current_low.index[-1], sup_line_col] = lows.lows_price.ix[
                    lows_diff_w_current_low.index[-1]]

                tl_df.loc[i, sup_line_col] = lows.lows_price.ix[i]

                tl_df[sup_line_col] = tl_df[sup_line_col].interpolate('barycentric').ix[i:]
                sup_tl_n += 1

        highs = tl_df[tl_df.highs == True]

        res_tl_n = 0

        for i in highs.index:
            if i != highs.index[0]:
                highs_diff_w_current_high = (highs.highs_price.ix[i] - highs.ix[:i].highs_price).abs().sort_values()
                tl_df['res_tl_' + str(res_tl_n)] = np.NaN

                tl_df.loc[highs_diff_w_current_high.index[-1], 'res_tl_' + str(res_tl_n)] = highs.highs_price.ix[
                    highs_diff_w_current_high.index[-1]]

                tl_df.loc[i, 'res_tl_' + str(res_tl_n)] = highs.highs_price.ix[i]

                tl_df['res_tl_' + str(res_tl_n)] = tl_df['res_tl_' + str(res_tl_n)].interpolate('barycentric').ix[i:]
                res_tl_n += 1
        return tl_df


    def calc_entryexit_rules(self, data, rolling_window_period, rules_index):

        tl_df = self.calc_trendlines(data.exo, rolling_window_period)

        tl_df['res_crossdown'] = False
        tl_df['res_crossup'] = False

        tl_df['sup_crossdown'] = False
        tl_df['sup_crossup'] = False

        res_tl_df = tl_df.filter(like='res_tl')
        sup_tl_df = tl_df.filter(like='sup_tl')

        for res_cols, sup_cols in zip(res_tl_df.columns, sup_tl_df.columns):
            res_crossdown = CrossDown(tl_df.px_ser, res_tl_df[res_cols])
            res_crossup = CrossUp(tl_df.px_ser, res_tl_df[res_cols])

            sup_crossdown = CrossDown(tl_df.px_ser, sup_tl_df[sup_cols])
            sup_crossup = CrossUp(tl_df.px_ser, sup_tl_df[sup_cols])

            for i in tl_df.index:
                if res_crossdown[i] == True:
                    if tl_df['res_crossdown'][i] == True:
                        pass

                    else:
                        tl_df.loc[i, 'res_crossdown'] = True

                if res_crossup[i] == True:
                    if tl_df['res_crossup'][i] == True:
                        pass

                    else:
                        tl_df.loc[i, 'res_crossup'] = True

                if sup_crossdown[i] == True:
                    if tl_df['sup_crossdown'][i] == True:
                        pass

                    else:
                        tl_df.loc[i, 'sup_crossdown'] = True

                if sup_crossup[i] == True:
                    if tl_df['sup_crossup'][i] == True:
                        pass

                    else:
                        tl_df.loc[i, 'sup_crossup'] = True

        tl_df = pd.concat([tl_df, data.exo], axis=1)

        if rules_index == 0:
            entry_rule = tl_df.sup_crossup

            exit_rule = tl_df.sup_crossdown
            return entry_rule, exit_rule

        if rules_index == 1:
            entry_rule = tl_df.sup_crossdown

            exit_rule = tl_df.sup_crossup
            return entry_rule, exit_rule

        if rules_index == 2:
            entry_rule = tl_df.res_crossup

            exit_rule = tl_df.res_crossdown
            return entry_rule, exit_rule

        if rules_index == 3:
            entry_rule = tl_df.res_crossdown

            exit_rule = tl_df.res_crossup
            return entry_rule, exit_rule

        if rules_index == 4:
            entry_rule = tl_df.res_crossdown

            exit_rule = tl_df.sup_crossup
            return entry_rule, exit_rule

        if rules_index == 5:
            entry_rule = tl_df.res_crossup

            exit_rule = tl_df.sup_crossdown
            return entry_rule, exit_rule

        if rules_index == 6:
            entry_rule = tl_df.sup_crossdown

            exit_rule = tl_df.res_crossup
            return entry_rule, exit_rule

        if rules_index == 7:
            entry_rule = tl_df.sup_crossup

            exit_rule = tl_df.res_crossdown
            return entry_rule, exit_rule

        if rules_index == 8:
            entry_rule = tl_df.lows

            exit_rule = tl_df.highs
            return entry_rule, exit_rule

        if rules_index == 9:
            entry_rule = tl_df.highs

            exit_rule = tl_df.lows
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
            direction, rolling_window_period, rules_index = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, rolling_window_period, rules_index = params

        # Defining EXO price
        px = self.data.exo

        # Enry/exit rules
        entry_rule, exit_rule = self.calc_entryexit_rules(self.data, rolling_window_period, rules_index)

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None
        if save_info:
            #calc_info = {'trailing_stop': trailing_stop}
            pass

        return swarm_member_name, entry_rule, exit_rule, calc_info

if __name__ == '__main__':
    from backtester.analysis import *
    from backtester.strategy import StrategyBase, OptParam, OptParamArray
    from backtester.swarms.ranking import SwarmRanker
    from backtester.swarms.rebalancing import SwarmRebalance
    from backtester.swarms.filters import SwarmFilter
    from backtester.costs import CostsManagerEXOFixed
    from backtester.exoinfo import EXOInfo
    from backtester.swarms.rankingclasses import *
    from backtester.swarms.swarm import Swarm
    from scripts.settings import *
    from exobuilder.data.exostorage import EXOStorage

    storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

    STRATEGY_CONTEXT = {
        'strategy': {
            'class': Strategy_SupRes_TrendLines,
            'exo_name': 'CL_ContFut',  # <---- Select and paste EXO name from cell above
            'exo_storage': storage,
            'opt_params': [
                # OptParam(name, default_value, min_value, max_value, step)
                OptParamArray('Direction', [1]),
                # OptParam('Min Max Rolling Window Period', 10, 5, 100, 10),
                OptParam('Min Max Rolling Window Period', 10, 10, 10, 4),
                OptParamArray('Rules index', [1])
                # OptParamArray('Rules index', np.arange(10))

            ],
        },
        'swarm': {
            'members_count': 1,
            'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
            'rebalance_time_function': SwarmRebalance.every_friday,

        },
        'costs': {
            'manager': CostsManagerEXOFixed,
            'context': {
                'costs_options': 3.0,
                'costs_futures': 3.0,
            }
        }
    }

    smgr = Swarm(STRATEGY_CONTEXT)
    #smgr.run_swarm()

    from backtester.reports.alpha_sanity_checks import AlphaSanityChecker


    # Testing trend lines algo for fut ref
    '''
    AlphaSanityChecker.test_algo(smgr.strategy.data.exo,                          # Source Data for algo
                                 AlphaSanityChecker.comp_results_dataframe,       # Comparison function
                                 smgr.strategy.calc_trendlines,                   # Algo to check
                                 10)                                              # Extra algo params (if required)
    '''

    #
    # Custom algorithm comparison function if algo returns custom type
    #
    def compare_entry_exit_rules(full, temp):
        entry_rule_full, exit_rule_full = full
        entry_rule_temp, exit_rule_temp = temp
        return AlphaSanityChecker.comp_results_series(entry_rule_full, entry_rule_temp) and \
               AlphaSanityChecker.comp_results_series(exit_rule_full, exit_rule_temp)

    AlphaSanityChecker.test_algo(smgr.strategy.data,
                                 compare_entry_exit_rules,
                                 smgr.strategy.calc_entryexit_rules, 10, 1)

    #asc = AlphaSanityChecker(smgr)
    #asc.run()