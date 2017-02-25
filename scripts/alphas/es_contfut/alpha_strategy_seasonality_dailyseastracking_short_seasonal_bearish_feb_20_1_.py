#
#
#  Automatically generated file 
#        Created at: 2017-02-21 19:45:57.920320
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_seasonality_dailyseastracking import Strategy_Seasonality_DailySeasTracking
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = Strategy_Seasonality_DailySeasTracking.name

STRATEGY_SUFFIX = "_Seasonal_Bearish_Feb_20_1_"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': Strategy_Seasonality_DailySeasTracking,
        'exo_name': 'ES_ContFut',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParamArray('Quandl data link', ['CHRIS/CME_ES1']), 
            OptParamArray('Starting year of hist. data', ['first+1', 2002, 1990, 2007]), 
            OptParamArray('Centered MA period', [3, 5]), 
            OptParamArray('Signals shift', [3, 7, 15]), 
            OptParamArray('Outliers reduction', [True]), 
            OptParamArray('Rules index', [1]), 
        ],
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
    },
}
