#
#
#  Automatically generated file 
#        Created at: 2017-02-20 17:05:39.586895
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_seasonality_dailyseastracking import Strategy_Seasonality_DailySeasTracking
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray


STRATEGY_NAME = Strategy_Seasonality_DailySeasTracking.name

STRATEGY_SUFFIX = "_Seasonal_Bullish_Feb_20_1_"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParamArray('Quandl data link', ['CHRIS/CME_S1']), 
            OptParamArray('Starting year of hist. data', ['first+1', 1990, 1995, 2002, 2007, 2008]), 
            OptParamArray('Centered MA period', [3]), 
            OptParamArray('Signals shift', [1]), 
            OptParamArray('Outliers reduction', [True]), 
            OptParamArray('Rules index', [1]), 
        ],
        'class': Strategy_Seasonality_DailySeasTracking,
        'exo_name': 'ZS_ContFut',
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
}
