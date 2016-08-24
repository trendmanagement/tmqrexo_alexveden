import numpy as np
import pandas as pd

class RankingClassBase():
    def __init__(self):
        pass

    def clear(self):
        raise NotImplementedError("Every Ranking class must implement clear() method")

    def rank(self, swarm_slice, nsystems):
        raise NotImplementedError("Every Ranking class must implement rank() method")


class RankerHighestReturns(RankingClassBase):
    def __init__(self, return_period):
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
