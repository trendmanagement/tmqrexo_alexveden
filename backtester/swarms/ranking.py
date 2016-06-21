
import numpy as np
import pandas as pd


class SwarmRanker(object):
    @staticmethod
    def highestreturns_14days(eqty, rebalance_time, context=None):
        '''
        Ranking function
        Calculate last 14 days equity returns, excluding out-of-market time
        :param eqty: Swarm member equity
        :param rebalance_time: rebalance time
        :param context: ranker function additional parameters
        :return: Series of metric which is used in ranking for swarm members
        '''
        return eqty.diff(periods=14)

    @staticmethod
    def highestreturns_max_sharpe(eqty, rebalance_time, context=None):
        '''
        Sharp based ranking function
        :param eqty: Swarm member equity
        :param rebalance_time: rebalance time
        :param context: ranker function additional parameters
        :return: Series of metric which is used in ranking for swarm members
        '''
        raise Exception("Obsolete must be rewritten to handle DataFrame")
        chg = eqty.diff(periods=14)

        sharpe = chg.rolling(200).mean() / chg.rolling(200).std()

        return pd.Series(sharpe*100, index=eqty.index)

    @staticmethod
    def highestreturns_14days_with_slopefilter(eqty, rebalance_time, context=None):
        '''
        Ranking function
        Calculate last 14 days equity returns, excluding out-of-market time
        :param eqty: Swarm member equity
        :param rebalance_time: rebalance time
        :param context: ranker function additional parameters
        :return: Series of metric which is used in ranking for swarm members
        '''
        q = eqty.rank(axis=1, pct=True)

        diff14 = eqty.diff(periods=14)
        ma90 = eqty.apply(lambda x: x.rolling(90).mean())

        rank = diff14
        # Filter all members with negative returns in 30 or 90 days
        rank[(eqty < ma90) | (ma90-ma90.shift(1) <= 0) | (eqty - eqty.shift(90) <= 0) | (q < 0.9)] = 0
        return rank

    @staticmethod
    def highestreturns_universal(eqty, rebalance_time, context=None):
        '''
        Ranking function
        Calculate last 14 days equity returns, excluding out-of-market time
        :param eqty: Swarm member equity
        :param rebalance_time: rebalance time
        :param context: ranker function additional parameters
        :return: Series of metric which is used in ranking for swarm members
        '''
        if context['ranking_type'] == 'relstr':
            #
            # Relative strength ranking type
            #
            relstr_ma_period = context['ranking_relstr_ma_period']
            ma = eqty.apply(lambda x: x.rolling(relstr_ma_period).mean())
            rank = eqty - ma

            # Filtering upper and lower bounds
            #rank_upper_bound = context['ranking_relstr_upperbound']
            #rank_lower_bound = context['ranking_relstr_lowerbound']
            #rank[(rank < rank_lower_bound) | (rank > rank_upper_bound)] = 0
        elif context['ranking_type'] == 'returns':
            #
            # Highest N-day equity returns ranking type
            #
            equity_returns_period = context['ranking_returns_period']
            rank = eqty.diff(periods=equity_returns_period)
        else:
            raise ValueError("Ranking type unknown")

        if 'ignore_eqty_less_ma' in context and context['ignore_eqty_less_ma']:
            ma_period = context['ignore_eqty_less_ma_period']
            ma = eqty.apply(lambda x: x.rolling(ma_period).mean())
            rank[eqty < ma] = 0
        if 'ignore_eqty_less_top_quantile' in context and context['ignore_eqty_less_top_quantile']:
            quantile = eqty.rank(axis=1, pct=True)
            quantile_threshold = context['ignore_eqty_less_top_quantile_threshold']
            rank[quantile < quantile_threshold] = 0
        if 'ignore_eqty_with_negative_ma_slope' in context and context['ignore_eqty_with_negative_ma_slope']:
            ma_period = context['ignore_eqty_with_negative_ma_period']
            slope_period = context['ignore_eqty_with_negative_ma_slope_period']
            ma = eqty.apply(lambda x: x.rolling(ma_period).mean())
            rank[(ma-ma.shift(slope_period) <= 0)] = 0
        if 'ignore_if_avg_swarm_negative_change' in context and context['ignore_if_avg_swarm_negative_change']:
            avg_chg_period = context['ignore_if_avg_swarm_negative_change_period']
            avgswarm = eqty.mean(axis=1)
            rank[avgswarm.diff(periods=avg_chg_period) <= 0] = 0
        if 'ignore_if_avg_swarm_negative_change' in context and context['ignore_if_avg_swarm_negative_change']:
            avg_chg_period = context['ignore_if_avg_swarm_negative_change_period']
            avgswarm = eqty.mean(axis=1)
            rank[avgswarm.diff(periods=avg_chg_period) <= 0] = 0

        return rank
