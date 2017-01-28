from backtester.analysis import *
from backtester.strategy import StrategyBase
import pandas as pd
import numpy as np


class Strategy_SupRes_HorLevels(StrategyBase):
    name = 'Strategy_SupRes_HorLevels'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    def calc_entryexit_rules(self, rollingminmax_period, rules_index):
        px_ser = self.data.exo

        sr_df = pd.DataFrame(px_ser, columns=['px_ser'])

        rollingmax = sr_df.px_ser.rolling(rollingminmax_period).max()
        rollingmin = sr_df.px_ser.rolling(rollingminmax_period).min()

        sr_df['highs'] = (rollingmax != sr_df.px_ser) & (rollingmax.shift(1) == sr_df.px_ser.shift(1))
        sr_df['lows'] = (rollingmin != sr_df.px_ser) & (rollingmin.shift(1) == sr_df.px_ser.shift(1))

        # sr_df['highs'] = (sr_df.px_ser < sr_df.px_ser.shift(1)) & (sr_df.px_ser.shift(1) > sr_df.px_ser.shift(2))
        # sr_df['lows'] = (sr_df.px_ser > sr_df.px_ser.shift(1)) & (sr_df.px_ser.shift(1) < sr_df.px_ser.shift(2))

        sr_df.loc[sr_df.lows == True, 'lows_price'] = rollingmin
        sr_df.loc[sr_df.highs == True, 'highs_price'] = rollingmax

        sr_df.ffill(inplace=True)

        for i in sr_df.px_ser.index:
            if sr_df['lows'][i] == True:
                sr_df['sup_level_' + str(sr_df.px_ser[i])] = pd.Series(sr_df.px_ser[i], index=sr_df.px_ser.ix[i:].index)

            if sr_df['highs'][i] == True:
                sr_df['res_level_' + str(sr_df.px_ser[i])] = pd.Series(sr_df.px_ser[i], index=sr_df.px_ser.ix[i:].index)

        sr_df['res_crossdown'] = False
        sr_df['res_crossup'] = False

        sr_df['sup_crossdown'] = False
        sr_df['sup_crossup'] = False

        res_levels_df = sr_df.filter(like='res_level')
        sup_levels_df = sr_df.filter(like='sup_level')

        for res_cols, sup_cols in zip(res_levels_df.columns, sup_levels_df.columns):
            res_crossdown = CrossDown(sr_df.px_ser, res_levels_df[res_cols])
            res_crossup = CrossUp(sr_df.px_ser, res_levels_df[res_cols])

            sup_crossdown = CrossDown(sr_df.px_ser, sup_levels_df[sup_cols])
            sup_crossup = CrossUp(sr_df.px_ser, sup_levels_df[sup_cols])

            for i in sr_df.index:
                if res_crossdown[i] == True:
                    if sr_df['res_crossdown'][i] == True:
                        pass

                    else:
                        sr_df.loc[i, 'res_crossdown'] = True

                if res_crossup[i] == True:
                    if sr_df['res_crossup'][i] == True:
                        pass

                    else:
                        sr_df.loc[i, 'res_crossup'] = True

                if sup_crossdown[i] == True:
                    if sr_df['sup_crossdown'][i] == True:
                        pass

                    else:
                        sr_df.loc[i, 'sup_crossdown'] = True

                if sup_crossup[i] == True:
                    if sr_df['sup_crossup'][i] == True:
                        pass

                    else:
                        sr_df.loc[i, 'sup_crossup'] = True

        # sr_df = pd.concat([sr_df, px_ser], axis=1)

        if rules_index == 0:
            entry_rule = sr_df.sup_crossup

            exit_rule = sr_df.sup_crossdown
            return entry_rule, exit_rule

        if rules_index == 1:
            entry_rule = sr_df.sup_crossdown

            exit_rule = sr_df.sup_crossup
            return entry_rule, exit_rule

        if rules_index == 2:
            entry_rule = sr_df.res_crossup

            exit_rule = sr_df.res_crossdown
            return entry_rule, exit_rule

        if rules_index == 3:
            entry_rule = sr_df.res_crossdown

            exit_rule = sr_df.res_crossup
            return entry_rule, exit_rule

        if rules_index == 4:
            entry_rule = sr_df.res_crossdown

            exit_rule = sr_df.sup_crossup
            return entry_rule, exit_rule

        if rules_index == 5:
            entry_rule = sr_df.res_crossup

            exit_rule = sr_df.sup_crossdown
            return entry_rule, exit_rule

        if rules_index == 6:
            entry_rule = sr_df.sup_crossdown

            exit_rule = sr_df.res_crossup
            return entry_rule, exit_rule

        if rules_index == 7:
            entry_rule = sr_df.sup_crossup

            exit_rule = sr_df.res_crossdown
            return entry_rule, exit_rule

        if rules_index == 8:
            entry_rule = sr_df.lows

            exit_rule = sr_df.highs
            return entry_rule, exit_rule

        if rules_index == 9:
            entry_rule = sr_df.highs

            exit_rule = sr_df.lows
            return entry_rule, exit_rule

        if rules_index == 10:
            entry_rule = (sr_df.px_ser < sr_df.highs_price) & (sr_df.px_ser < sr_df.lows_price)

            exit_rule = (sr_df.px_ser > sr_df.highs_price) & (sr_df.px_ser > sr_df.lows_price)
            return entry_rule, exit_rule

        if rules_index == 11:
            entry_rule = (sr_df.px_ser > sr_df.highs_price) & (sr_df.px_ser > sr_df.lows_price)

            exit_rule = (sr_df.px_ser < sr_df.highs_price) & (sr_df.px_ser < sr_df.lows_price)
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
            direction, rollingminmax_period, rules_index = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, rollingminmax_period, rules_index = params

        # Defining EXO price
        px = self.data.exo

        # Enry/exit rules
        entry_rule, exit_rule = self.calc_entryexit_rules(rollingminmax_period, rules_index)

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

    try:
        from scripts.settings_local import *
    except:
        pass

    from exobuilder.data.exostorage import EXOStorage

    storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

    STRATEGY_CONTEXT = {
        'strategy': {
            'class': Strategy_SupRes_HorLevels,
            'exo_name': 'CL_ContFut',  # <---- Select and paste EXO name from cell above
            'exo_storage': storage,
            'opt_params': [
                # OptParam(name, default_value, min_value, max_value, step)
                OptParamArray('Direction', [-1]),
                OptParam('Rolling Min/Max period', 10, 42, 42, 4),
                OptParamArray('Rules index', [9])
                # OptParamArray('Rules index', np.arange(12))

            ],
        },
        'swarm': {
            'members_count': 1,
            'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
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
    smgr.run_swarm()