#
#
#  Automatically generated file 
#        Created at: 2017-02-20 15:42:25.961829
#
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_seasonality_dailyseastracking import Strategy_Seasonality_DailySeasTracking
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = Strategy_Seasonality_DailySeasTracking.name

STRATEGY_SUFFIX = "_Seasonal_Bullish_Feb_20_1"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'exo_name': 'ZC_ContFut',
        'class': Strategy_Seasonality_DailySeasTracking,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParamArray('Quandl data link', ['CHRIS/CME_C1']), 
            OptParamArray('Starting year of hist. data', ['first+1', 1990, 2000, 1995, 2002, 2007, 2008]), 
            OptParamArray('Centered MA period', [5]), 
            OptParamArray('Signals shift', [5]), 
            OptParamArray('Outliers reduction', [True]), 
            OptParamArray('Rules index', [1]), 
        ],
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
    },
}
