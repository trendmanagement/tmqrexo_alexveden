#
#
#  Automatically generated file 
#        Created at: 2017-02-20 16:27:34.764809
#
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_seasonality_dailyseastracking import Strategy_Seasonality_DailySeasTracking
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray


STRATEGY_NAME = Strategy_Seasonality_DailySeasTracking.name

STRATEGY_SUFFIX = "_Seasonal_Bearish_Feb_20_0_"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'NG_ContFut',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParamArray('Quandl data link', ['CHRIS/CME_NG1']), 
            OptParamArray('Starting year of hist. data', ['first+1', 1990, 1995, 2002, 2007, 1997]), 
            OptParamArray('Centered MA period', [2]), 
            OptParamArray('Signals shift', [1]), 
            OptParamArray('Outliers reduction', [True]), 
            OptParamArray('Rules index', [0]), 
        ],
        'class': Strategy_Seasonality_DailySeasTracking,
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
