cimport cython
import numpy as np
import pandas as pd
cimport numpy as np
DTYPE_float = np.float
ctypedef np.float64_t DTYPE_t_float
ctypedef np.uint64_t DTYPE_t_uint64
ctypedef np.uint8_t DTYPE_t_uint8
from libc.math cimport abs, isnan
import warnings

np.import_array()


@cython.cdivision(True)
@cython.boundscheck(False)
def backtest(data,
             np.ndarray[DTYPE_t_uint8, ndim=1, cast=True] entry_rule,
             np.ndarray[DTYPE_t_uint8, ndim=1, cast=True] exit_rule,
             int direction):
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
    cdef np.ndarray[DTYPE_t_float, ndim=1] price = data['exo'].values

    cdef int inpos = 0
    cdef int i = 0
    cdef float pnl = 0.0
    cdef float px = 0.0
    cdef int barcount = price.shape[0]


    cdef np.ndarray[DTYPE_t_float, ndim=1] pl = np.zeros(barcount)
    cdef np.ndarray[DTYPE_t_uint8, ndim=1] inpositon = np.zeros(barcount, dtype=np.uint8)



    for i in range(barcount):
        if inpos == 0:
            # We have a signal, let's open position
            if entry_rule[i] == 1:
                pl[i] = 0
                inpos = 1
                inpositon[i] = 1
            else:
                inpositon[i] = 0

        else:
            # Calculate pl
            pl[i] = (price[i] - price[i-1]) * direction

            if exit_rule[i] == 1:
                inpos = 0
                inpositon[i] = 0
            else:
                inpositon[i] = 1

    return pd.Series(pl, index=data.index), pd.Series(inpositon, index=data.index)


def calc_costs(float transaction_costs,float rollover_costs, float prev_exp, float current_exp):
    # If rollover occurred
    cdef float _costs_value = 0.0
    if rollover_costs != 0:
        _costs_value += (-abs(rollover_costs) * abs(prev_exp))

    _costs_value += (-abs(transaction_costs) * abs(prev_exp - current_exp))

    return _costs_value


@cython.cdivision(True)
@cython.boundscheck(False)
def stats_exposure(exo_dataframe, exposure, costs=None, extendedstats=False):
    """
    Calculate equity and summary statistics, based on output of `backtest` method
    :param exo_dataframe: price of EXO or another asset
    :param exposure: exposure of asset
    :param costs: transaction costs expressed as base points of price
    :param extendedstats: calculate extended stats (like delta, costs values and etc)
    :return: tuple (equity, stats)
        - equity - is cumulative profits array
        - stats - is a dict() if extendedstats=True
    """
    # Calculate trade-by-trade payoffs
    cdef float profit = 0.0
    cdef int entry_i = -1
    cdef float barsintrade = 0.0
    cdef float summae = 0.0
    cdef float mae = 0.0
    cdef float costs_sum = 0.0

    cdef np.ndarray[DTYPE_t_float, ndim=1] _price = exo_dataframe['exo'].values
    cdef np.ndarray[DTYPE_t_float, ndim=1] _delta
    cdef np.ndarray[DTYPE_t_float, ndim=1] _exposure

    try:
        _exposure = exposure.values
    except AttributeError:
        _exposure = exposure

    cdef int barcount = _price.shape[0]

    cdef np.ndarray[DTYPE_t_float, ndim=1] result_equity = np.zeros(barcount)
    cdef np.ndarray[DTYPE_t_float, ndim=1] result_costs = np.zeros(barcount)

    cdef int i = 0
    cdef int v = 0
    cdef float _costs_value = 0.0
    cdef float current_exp = 0.0
    cdef float prev_exp = 0.0

    cdef int has_costs = costs is not None


    cdef np.ndarray[DTYPE_t_float, ndim=1] rollover_costs
    cdef np.ndarray[DTYPE_t_float, ndim=1] transaction_costs

    if has_costs:
        rollover_costs = costs['rollover_costs'].values
        transaction_costs = costs['transaction_costs'].values

    for i in range(1, barcount):
        # Calculate cumulative profit inside particular trade
        current_exp = _exposure[i]
        prev_exp = _exposure[i-1]

        profit = (_price[i] - _price[i-1]) * prev_exp

        # Apply transaction costs
        if has_costs:
            _costs_value = calc_costs(transaction_costs[i], rollover_costs[i], prev_exp, current_exp)
            profit += _costs_value
            result_costs[i] = _costs_value

        result_equity[i] = result_equity[i-1] + profit

    results_series_dict = {'equity': result_equity}

    result_stats_dict = {}

    if extendedstats:
        # Calculate extended stats
        results_series_dict['costs'] = result_costs
        if 'delta' not in exo_dataframe:
            # Old exo data array (need to rebuild EXO data)
            warnings.warn("EXO data frame doesn't contain 'delta' series, you should rebuild EXO data to get delta information")
            results_series_dict['delta'] = pd.Series(np.zeros(barcount), index=exo_dataframe.index)
        else:
            # Delta array is present in EXO dataframe
            i = 0
            _delta = exo_dataframe['delta'].values
            results_series_dict['delta']  = pd.Series(_delta * _exposure, index=exo_dataframe.index)

    return pd.DataFrame(results_series_dict, index=exo_dataframe.index), result_stats_dict



@cython.cdivision(True)
@cython.boundscheck(False)
def backtest_equity(df):
    """
    Quick backtest function based on equity (used by ranking algorithm)
    :param df:
    :return:
    """

    # Calculate trade-by-trade payoffs
    cdef float netprofit = 0.0
    cdef float sumwin = 0.0
    cdef float sumloss = 0.0
    cdef float wincount = 0.0
    cdef float tradescount = 0.0
    cdef float eqhigh = 0.0
    cdef float maxdd = 0.0
    cdef float px_chg = 0.0


    cdef np.ndarray[DTYPE_t_float, ndim=1] px = df.values
    cdef int barcount = px.shape[0]

    cdef int i = 1

    for i in range(1, barcount):
        px_chg = px[i] - px[i-1]

        netprofit += px_chg

        eqhigh = max(eqhigh, netprofit)
        maxdd = min(maxdd, netprofit - eqhigh)

        if px_chg > 0:
            wincount += 1.0
            sumwin += px_chg
        else:
            sumloss += px_chg

        tradescount += 1.0

    try:
        modsharpe = np.mean(px) / np.std(px)
    except ZeroDivisionError:
        modsharpe = np.nan

    return {'strategy': df.name,
            'stats_pricechange_modsharpe': modsharpe,
            'stats_netprofit': netprofit,
            'stats_max_dd': maxdd,
            'stats_recovery_factor': netprofit / abs(maxdd),
            'stats_profit_factor': sumwin / abs(sumloss),
            'stats_winrate': wincount / tradescount
            }