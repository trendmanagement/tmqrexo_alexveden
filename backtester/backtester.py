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
            pl.values[i] = (price.values[i] - price.values[i-1]) * direction
            inpositon.values[i] = 1

            if exit_rule.values[i] == 1:
                inpos = False

    return pl, inpositon


def stats(pl, inposition, positionsize=None, costs=None):
    """
    Calculate equity and summary statistics, based on output of `backtest` method
    :param pl: Profit-loss array (returned by backtest())
    :param inposition: In-position array (returned by backtest())
    :param positionsize: Value of position size (by default is: 1.0)
    :param costs: transaction costs expressed as base points of price
    :return: tuple (equity, stats)
        - equity - is cumulative profits array
        - stats - is a dict()
    """
    # Calculate trade-by-trade payoffs
    trades = []
    profit = 0.0
    entry_i = -1
    barsintrade = 0.0
    summae = 0.0
    mae = 0.0

    equity = np.zeros(len(inposition))

    for i, v in enumerate(inposition):
        if i == 0:
            continue

        # Calculate cumulative profit inside particular trade
        if inposition.values[i] == 1:
            if inposition.values[i-1] == 0:
                # Store index of entry point
                entry_i = i
                equity[i] = equity[i-1]
                mae = 0.0

            # Calculate position size it may be used for
            # - Volatility adjusted sizing
            # - Taking into account pointvalue > 1.0
            # For compatibility with old code, we use 1.0 by default
            psize = 1.0
            if positionsize is not None:
                    if np.isnan(positionsize.values[entry_i]):
                        continue
                    psize = positionsize.values[entry_i]

            # Apply transaction costs
            # Apply on entry point
            if costs is not None and i == entry_i:
                profit += (-np.abs(costs.values[i]) * psize * 2)

            profit += pl.values[i] * psize

            mae = min(profit, mae)

            equity[i] = equity[entry_i] + profit

        # Store result
        if inposition.values[i] == 0:
            if inposition.values[i-1] == 1:
                # Apply transaction costs
                if costs is not None:
                    # Taking all costs at trade open
                    #profit += -np.abs(costs.values[i-1]) * psize
                    pass
                mae = min(profit, mae)
                # Taking costs into account at exit
                equity[i-1] = equity[entry_i] + profit

                summae += mae
                barsintrade += (i-1)-entry_i
                trades.append(profit)
                profit = 0.0

            # Continuing equity line if no trades
            equity[i] = equity[i-1]


    trades = pd.Series(trades)

    equity = pd.Series(equity, index=inposition.index)
    trades_equity = trades.cumsum()

    # Calculate summary statistics
    if len(trades) == 0:
        statsistics = None
    else:
        statsistics = {
            'netprofit': np.sum(trades),
            'avg': np.mean(trades),
            'std': np.std(trades),
            'count': len(trades),
            'winrate': len(trades[trades > 0]) / len(trades),
            'maxdd': (equity - equity.expanding().max()).min(),
            'avgbarsintrade': barsintrade / len(trades)-1,
            'avgmae': summae / len(trades),
            'tradesmaxdd':  (trades_equity - trades_equity.expanding().max()).min(),
        }
    return equity, statsistics


def trades(pl, inposition):
    """
    Calculate closed trades array
    :param pl: Profit-loss array (returned by backtest())
    :param inposition: In-position array (returned by backtest())
    :return: trades array
    """
    # Calculate trade-by-trade payoffs
    trades = np.empty(len(pl))
    trades.fill(np.nan)

    profit = 0.0
    for i, v in enumerate(inposition):
        if i == 0:
            continue
        # Calculate cumulative profit inside particular trade
        if inposition.values[i] == 1:
            profit += pl.values[i]
        # Store result
        if inposition.values[i] == 0 and inposition.values[i-1] == 1:
            trades[i] = profit
            profit = 0.0

    return pd.Series(trades, index=pl.index)

