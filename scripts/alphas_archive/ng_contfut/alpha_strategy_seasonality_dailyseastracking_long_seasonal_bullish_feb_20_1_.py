#
#
#  Automatically generated file 
#        Created at: 2017-02-20 16:33:26.223543
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray
from strategies.strategy_seasonality_dailyseastracking import Strategy_Seasonality_DailySeasTracking
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = Strategy_Seasonality_DailySeasTracking.name

STRATEGY_SUFFIX = "_Seasonal_Bullish_Feb_20_1_"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'class': Strategy_Seasonality_DailySeasTracking,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParamArray('Quandl data link', ['CHRIS/CME_NG1']), 
            OptParamArray('Starting year of hist. data', ['first+1', 1990, 1995, 2002, 2007, 1997]), 
            OptParamArray('Centered MA period', [5]), 
            OptParamArray('Signals shift', [1, 3]), 
            OptParamArray('Outliers reduction', [True]), 
            OptParamArray('Rules index', [1]), 
        ],
        'exo_name': 'NG_ContFut',
    },
}
