#
#
#  Automatically generated file 
#        Created at: 2017-02-20 17:10:38.359342
#
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_seasonality_dailyseastracking import Strategy_Seasonality_DailySeasTracking
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray


STRATEGY_NAME = Strategy_Seasonality_DailySeasTracking.name

STRATEGY_SUFFIX = "_Seasonal_Bearish_Feb_20_1_"

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
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
    'strategy': {
        'class': Strategy_Seasonality_DailySeasTracking,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParamArray('Quandl data link', ['CHRIS/CME_S1']), 
            OptParamArray('Starting year of hist. data', ['first+1', 1990, 1995, 2002, 2007, 1997]), 
            OptParamArray('Centered MA period', [2, 5]), 
            OptParamArray('Signals shift', [4, 7]), 
            OptParamArray('Outliers reduction', [True]), 
            OptParamArray('Rules index', [1]), 
        ],
        'exo_name': 'ZS_ContFut',
    },
}
