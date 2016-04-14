import pandas as pd
import numpy as np


def backtest(data, entry_rule, exit_rule, direction):
    """
    Backtester routine calculate equity based on data['exo'] and entry/exit rules
    :param data: raw data for backtesting
    :param entry_rule: 1/0 array of entry points
    :param exit_rule: 1/0 array of exit points
    :param direction: Direction of trades, 1 - for long, -1 - for shorts
    :return: tuple(pl, inposition)
        pl - profit-loss inside a particular trade
        inposition - 1/0 array indicating whether the EXO is in or out of the market at the end of the day
    """

    price = data['exo']
    pl = pd.Series(np.zeros(len(price.index)), index=price.index)
    inpositon = pd.Series(np.zeros(len(price.index)), index=price.index)

    inpos = False

    for i, px in enumerate(price):
        if not inpos:
            # We have a signal, let's open position
            if entry_rule.values[i] == 1:
                pl.values[i] = 0
                inpos = True
                inpositon.values[i] = 1
            else:
                inpositon.values[i] = 0

        else:
            # Calculate pl
            pl.values[i] = (price.values[i] - price.values[i-1])*direction
            inpositon.values[i] = 1

            if exit_rule.values[i] == 1:
                inpos = False

    return pl, inpositon


def stats(pl, inposition):
    """
    Calculate equity and summary statistics, based on output of `backtest` method
    :param pl: Profit-loss array (returned by backtest())
    :param inposition: In-position array (returned by backtest())
    :return: tuple (equity, stats)
        - equity - is cumulative profits arrat
        - stats - is a dict()
    """

    # Calculate cumulative equity of pl
    # We are dropping all empty values at first
    equity = pl.dropna().cumsum()

    # Calculate trade-by-trade payoffs
    trades = []
    profit = 0.0
    for i, v in enumerate(inposition):
        if i == 0:
            continue
        # Calculate cumulative profit inside particular trade
        if inposition.values[i] == 1:
            profit += pl.values[i]
        # Store result
        if inposition.values[i] == 0 and inposition.values[i-1] == 1:
            trades.append(profit)
            profit = 0.0
    trades = np.array(trades)

    # Calculate summary statistics
    statsistics = {
        'netprofit': np.sum(trades),
        'avg': np.mean(trades),
        'std': np.std(trades),
        'count': len(trades),
        'winrate': len(trades[trades > 0]) / len(trades),
        'maxdd': (equity - pd.expanding_max(equity)).min(),
    }
    return equity, statsistics
