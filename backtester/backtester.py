import pandas as pd
import numpy as np


def backtest(data, entry_rule, exit_rule, direction):
    """
    Backtester routine calculate equity based on data['exo'] and entry/exit rules
    :param data:
    :param entryrule:
    :return:
    """

    price = data['exo']
    pl = pd.Series(index=price.index)
    inpositon = pd.Series(index=price.index)

    start_idx = -1
    inpos = False

    for i, px in enumerate(price):
        if not inpos:
            # We have a signal, let's open position
            if entry_rule.values[i] == 1:
                start_idx = i
                pl.values[i] = 0
                inpos = True
                inpositon.values[i] = 1
            else:
                inpositon.values[i] = 0

        else:
            # Calculate pl
            pl.values[i] = (price.values[i] - price.values[start_idx])*direction
            inpositon.values[i] = 1

            if exit_rule.values[i] == 1:
                start_idx = -1
                inpos = False

    return pl, inpositon