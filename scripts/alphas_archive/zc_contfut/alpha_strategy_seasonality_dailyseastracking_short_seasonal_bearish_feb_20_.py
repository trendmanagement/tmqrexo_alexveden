#
#
#  Automatically generated file 
#        Created at: 2017-02-20 15:38:13.684175
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_seasonality_dailyseastracking import Strategy_Seasonality_DailySeasTracking
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = Strategy_Seasonality_DailySeasTracking.name

STRATEGY_SUFFIX = "_Seasonal_Bearish_Feb_20_"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'strategy': {
        'class': Strategy_Seasonality_DailySeasTracking,
        'exo_name': 'ZC_ContFut',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParamArray('Quandl data link', ['CHRIS/CME_C1']), 
            OptParamArray('Starting year of hist. data', ['first+1', 1990, 2000, 2008, 2002, 1995]), 
            OptParamArray('Centered MA period', [5, 3]), 
            OptParamArray('Signals shift', [5]), 
            OptParamArray('Outliers reduction', [True]), 
            OptParamArray('Rules index', [0]), 
        ],
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
