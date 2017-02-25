#
#
#  Automatically generated file 
#        Created at: 2017-02-21 19:36:46.410594
#
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_seasonality_dailyseastracking import Strategy_Seasonality_DailySeasTracking


STRATEGY_NAME = Strategy_Seasonality_DailySeasTracking.name

STRATEGY_SUFFIX = "_Seasonal_Bearish_Feb_20_0"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParamArray('Quandl data link', ['CHRIS/CME_CL1']), 
            OptParamArray('Starting year of hist. data', ['first+1', 1995, 1990, 1997, 2007]), 
            OptParamArray('Centered MA period', [1, 3]), 
            OptParamArray('Signals shift', [2, 7]), 
            OptParamArray('Outliers reduction', [True]), 
            OptParamArray('Rules index', [0]), 
        ],
        'exo_name': 'CL_ContFut',
        'class': Strategy_Seasonality_DailySeasTracking,
    },
}
