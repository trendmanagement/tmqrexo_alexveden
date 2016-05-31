import pandas as pd


class SwarmRebalance(object):
    @ staticmethod
    def norebalance(swarm):
        """
        For testing purposes
        :param swarm:
        :return:
        True|False - array (swarm.index shape)
        """
        res = pd.Series(0, index=swarm.index)
        res.values[102] = 1

        return res

    @ staticmethod
    def every_month(swarm):
        """
        Swarm rebalance function 'every new month'
        :param swarm:
        :return:
        True|False - array (swarm.index shape)
        """
        month = pd.Series(swarm.index.month)
        return pd.Series(1, index=swarm.index)

    @ staticmethod
    def every_monday(swarm):
        """
        Swarm rebalance function 'every week on monday'
        :param swarm:
        :return:
        True|False - array (swarm.index shape)
        """
        return pd.Series(swarm.index.dayofweek == 0, index=swarm.index)