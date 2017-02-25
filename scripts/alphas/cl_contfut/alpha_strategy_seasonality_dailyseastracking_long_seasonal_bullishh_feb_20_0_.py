#
#
#  Automatically generated file 
#        Created at: 2017-02-21 19:32:50.796807
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_seasonality_dailyseastracking import Strategy_Seasonality_DailySeasTracking
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = Strategy_Seasonality_DailySeasTracking.name

STRATEGY_SUFFIX = "_Seasonal_Bullishh_Feb_20_0_"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'exo_name': 'CL_ContFut',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParamArray('Quandl data link', ['CHRIS/CME_CL1']), 
            OptParamArray('Starting year of hist. data', ['first+1', 1995, 2008]), 
            OptParamArray('Centered MA period', [1, 3]), 
            OptParamArray('Signals shift', [1, 3]), 
            OptParamArray('Outliers reduction', [True]), 
            OptParamArray('Rules index', [0]), 
        ],
        'class': Strategy_Seasonality_DailySeasTracking,
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
}
