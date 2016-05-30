import pandas as pd

def rebalance_norebalance(swarm):
    """
    For testing purposes
    :param swarm:
    :return:
    True|False - array (swarm.index shape)
    """
    res = pd.Series(0, index=swarm.index)
    res.values[102] = 1

    return res

def rebalance_every_month(swarm):
    """
    Swarm rebalance function 'every new month'
    :param swarm:
    :return:
    True|False - array (swarm.index shape)
    """
    month = pd.Series(swarm.index.month)
    return pd.Series(1, index=swarm.index)

def rebalance_every_monday(swarm):
    """
    Swarm rebalance function 'every week on monday'
    :param swarm:
    :return:
    True|False - array (swarm.index shape)
    """
    return pd.Series(swarm.index.dayofweek == 0, index=swarm.index)