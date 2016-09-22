import numpy as np
import pandas as pd
from scipy.stats.stats import pearsonr

import pyximport
pyximport.install()
from backtester.backtester_fast import backtest_equity

class RankingClassBase():
    def __init__(self):
        pass

    def clear(self):
        raise NotImplementedError("Every Ranking class must implement clear() method")

    def rank(self, swarm_slice, nsystems):
        raise NotImplementedError("Every Ranking class must implement rank() method")

    def __str__(self):
        return 'RankingClassBase'


class RankerHighestReturns(RankingClassBase):
    def __init__(self, return_period):
        super().__init__()
        self.return_period = abs(return_period)

    def clear(self):
        pass

    def rank(self, swarm_slice, nsystems):
        result = []
        rank_info = []
        # Select required window for calculations
        ss = swarm_slice.iloc[-self.return_period-10:, :]

        # Calculate 14-period equity returns and sort values
        last_diff = ss.diff(periods=self.return_period).iloc[-1, :].sort_values(ascending=False).dropna()

        # Pick best nsystems
        best = last_diff[:nsystems]

        for k, v in best.items():
            if not np.isnan(v) and v > 0:
                result.append(k)
                rank_info.append({'rank_value': v})

        return result, rank_info

    def __str__(self):
        return 'RankerHighestReturns(return_period={0})'.format(self.return_period)


class RankerBestWithCorrel(RankingClassBase):
    def __init__(self, window_size=-1, correl_threshold=0.5):
        """
        2 Step ranking function
        1-Step: pick best systems by SUM(PercentRanks(Netprofit, MDD, Sharpe, RecoveryFactor, P))
        2-Step: pick systems with correlation < correl_threshold
        :param window_size: Size of window. -1 = Expandind window, >0 = Rolling window size (in days)
        :param correl_threshold: correlation threshold
        """
        super().__init__()
        self.window_size = window_size
        self.correl_threshold = correl_threshold

    def clear(self):
        pass

    def __str__(self):
        return 'RankerBestWithCorrel(window_size={0}, correl_threshold={1})'.format(self.window_size, self.correl_threshold)

    def rank(self, swarm_slice, nsystems):
        # Filter all negative equities
        ss = swarm_slice[(swarm_slice.iloc[-1][(swarm_slice.iloc[-1] > 0)]).index]
        if self.window_size > 0:
            # Use rolling window of self.window_size days length
            ss = ss.iloc[-self.window_size:]

        if len(ss.columns) == 0:
            return [], []

        # Applying simple backtesting function
        bt_data = ss.apply(backtest_equity)

        # Creating dataframe for new backtest metrics values
        stats_df = pd.DataFrame([x for x in bt_data])
        stats_df = stats_df.set_index('strategy')

        # Calculating ranking for Sum(ranks)
        best_stats = (stats_df.rank(pct=True)).sum(axis=1).sort_values(ascending=False)

        if not np.isnan(best_stats[0]) and best_stats[0] <= 0:
            return [], []

        # Picking N best system with low correlation
        best_systems = []
        best_systems.append(best_stats.index[0])

        i = 1
        corr_threshold = self.correl_threshold

        while i < len(best_stats) and len(best_systems) < nsystems:
            best = best_systems[-1]
            candidate = best_stats.index[i]
            # Calculate Pearson correlation of equity lines
            corr = pearsonr(ss[best].values, ss[candidate].values)[0]

            # If correlation between last and candidate system equity < threshold
            if not np.isnan(corr) and corr < corr_threshold:
                best_systems.append(candidate)
            i += 1

        rank_info = {
            'start_of_window': ss.index[0],
            'end_of_window': ss.index[-1],
            'corr_matrix': ss[best_systems].corr()
        }

        return best_systems, rank_info