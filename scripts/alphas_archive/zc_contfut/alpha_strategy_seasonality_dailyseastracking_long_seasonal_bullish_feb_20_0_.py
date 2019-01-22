#
#
#  Automatically generated file 
#        Created at: 2017-02-20 15:47:13.381737
#
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_seasonality_dailyseastracking import Strategy_Seasonality_DailySeasTracking
from backtester.strategy import OptParamArray
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = Strategy_Seasonality_DailySeasTracking.name

STRATEGY_SUFFIX = "_Seasonal_Bullish_Feb_20_0_"

STRATEGY_CONTEXT = {
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'class': Strategy_Seasonality_DailySeasTracking,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParamArray('Quandl data link', ['CHRIS/CME_C1']), 
            OptParamArray('Starting year of hist. data', ['first+1', 1990, 2000, 2008]), 
            OptParamArray('Centered MA period', [3]), 
            OptParamArray('Signals shift', [2]), 
            OptParamArray('Outliers reduction', [True]), 
            OptParamArray('Rules index', [0]), 
        ],
        'exo_name': 'ZC_ContFut',
    },
}
