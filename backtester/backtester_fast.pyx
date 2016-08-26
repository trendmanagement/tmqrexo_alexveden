cimport cython
import numpy as np
import pandas as pd
cimport numpy as np
DTYPE_float = np.float
ctypedef np.float64_t DTYPE_t_float
ctypedef np.uint64_t DTYPE_t_uint64
ctypedef np.uint8_t DTYPE_t_uint8
from libc.math cimport abs, isnan

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


@cython.cdivision(True)
@cython.boundscheck(False)
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
    cdef float profit = 0.0
    cdef int entry_i = -1
    cdef float barsintrade = 0.0
    cdef float summae = 0.0
    cdef float mae = 0.0
    cdef float costs_sum = 0.0

    cdef np.ndarray[DTYPE_t_float, ndim=1] _pl = pl.values
    cdef np.ndarray[DTYPE_t_uint8, ndim=1] _inposition = inposition.values

    cdef int barcount = _pl.shape[0]

    cdef np.ndarray[DTYPE_t_float, ndim=1] equity = np.zeros(barcount)

    cdef int i = 0
    cdef int v = 0
    cdef float psize = 0.0
    cdef float _costs_value = 0.0

    cdef int has_possize = positionsize is not None
    cdef int has_costs = costs is not None

    cdef np.ndarray[DTYPE_t_float, ndim=1] _positionsize
    cdef np.ndarray[DTYPE_t_float, ndim=1] _costs

    if has_possize:
        _positionsize = positionsize.values
    if has_costs:
        _costs = costs.values

    for i in range(1, barcount):
        # Calculate cumulative profit inside particular trade
        if _inposition[i] == 1:
            # Calculate position size it may be used for
            # - Volatility adjusted sizing
            # - Taking into account pointvalue > 1.0
            # For compatibility with old code, we use 1.0 by default
            psize = 1.0
            if has_possize:
                if isnan(_positionsize[entry_i]):
                    continue
                psize = _positionsize[entry_i]


            if _inposition[i-1] == 0:
                # Store index of entry point
                entry_i = i
                equity[i] = equity[i-1]
                mae = 0.0
                # Important hack!
                # When we apply global_filter
                # PL on entry point must be 0
                profit = 0.0
            else:
                profit += _pl[i] * psize


            # Apply transaction costs
            # Apply on entry point
            if has_costs and i == entry_i:
                _costs_value = (-abs(_costs[i]) * psize * 2)
                costs_sum +=_costs_value
                profit += _costs_value

            mae = min(profit, mae)

            equity[i] = equity[entry_i-1] + profit

        # Store result
        if _inposition[i] == 0:
            if _inposition[i-1] == 1:
                profit += _pl[i] * psize
                equity[i] = equity[entry_i - 1] + profit
                summae += mae
                barsintrade += (i-1)-entry_i
                profit = 0.0
            else:
                # Continuing equity line if no trades
                equity[i] = equity[i-1]

    return pd.Series(equity, index=inposition.index), None

@cython.cdivision(True)
@cython.boundscheck(False)
def stats_exposure(price, exposure, costs=None, extendedstats=False):
    """
    Calculate equity and summary statistics, based on output of `backtest` method
    :param price: price of EXO or another asset
    :param exposure: exposure of asset
    :param costs: transaction costs expressed as base points of price
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

    cdef np.ndarray[DTYPE_t_float, ndim=1] _price = price.values
    cdef np.ndarray[DTYPE_t_float, ndim=1] _exposure

    try:
        _exposure = exposure.values
    except AttributeError:
        _exposure = exposure

    cdef int barcount = _price.shape[0]

    cdef np.ndarray[DTYPE_t_float, ndim=1] equity = np.zeros(barcount)

    cdef int i = 0
    cdef int v = 0
    cdef float _costs_value = 0.0
    cdef psize = 0.0

    cdef int has_costs = costs is not None

    cdef np.ndarray[DTYPE_t_float, ndim=1] _costs

    if has_costs:
        _costs = costs.values

    for i in range(1, barcount):
        # Calculate cumulative profit inside particular trade
        current_exp = _exposure[i]
        prev_exp = _exposure[i-1]

        profit = (_price[i] - _price[i-1]) * prev_exp

        # Apply transaction costs
        # Apply on entry point
        if has_costs and current_exp != prev_exp:
            _costs_value = (-abs(_costs[i]) * abs(prev_exp-current_exp))
            profit += _costs_value

        equity[i] = equity[i-1] + profit
        '''
            # Apply transaction costs
            # Apply on entry point
            if has_costs and i == entry_i:
                _costs_value = (-abs(_costs[i]) * psize * 2)
                costs_sum +=_costs_value
                profit += _costs_value

            equity[i] = equity[entry_i-1] + profit
        '''

    return pd.Series(equity, index=price.index), {'note:' 'Not implemented yet'}