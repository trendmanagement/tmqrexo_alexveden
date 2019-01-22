#
#
#  Automatically generated file 
#        Created at: 2017-02-20 15:45:06.763632
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_seasonality_dailyseastracking import Strategy_Seasonality_DailySeasTracking
from backtester.strategy import OptParamArray


STRATEGY_NAME = Strategy_Seasonality_DailySeasTracking.name

STRATEGY_SUFFIX = "_Seasonal_Bearish_Feb_20_1_"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'members_count': 1,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'strategy': {
        'exo_name': 'ZC_ContFut',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParamArray('Quandl data link', ['CHRIS/CME_C1']), 
            OptParamArray('Starting year of hist. data', ['first+1', 1990, 2000]), 
            OptParamArray('Centered MA period', [3, 10]), 
            OptParamArray('Signals shift', [2, 3]), 
            OptParamArray('Outliers reduction', [True]), 
            OptParamArray('Rules index', [1]), 
        ],
        'class': Strategy_Seasonality_DailySeasTracking,
    },
}
