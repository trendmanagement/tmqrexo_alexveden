# Importing EXO code
from exobuilder.algorithms.exo_brokenwing import EXOBrokenwingCollar
from exobuilder.algorithms.exo_vertical_spread import EXOVerticalSpread
from exobuilder.algorithms.exo_continous_fut import EXOContinuousFut
from exobuilder.algorithms.smartexo_ichimoku_bear_straddle_150delta import SmartexoIchimokuBearStraddle150Delta
from exobuilder.algorithms.smartexo_ichi_bullish_straddle_150delta_exphedged_nov22_2016 import SmartEXOIchiBullishStraddle150DeltaExpHedgedNov22_2016
from exobuilder.algorithms.SmartEXO_Ichi_DeltaTargeting_Dec3_Bear_Bear_Spread import SmartEXO_Ichi_DeltaTargeting_Dec3_Bear_Bear_Spread
from exobuilder.algorithms.SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread import SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread
from exobuilder.algorithms.SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread import SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread

#
# Instruments list
#
INSTRUMENTS_LIST = ['ES', 'CL', 'NG', 'ZN', 'ZS', 'ZW', 'ZC']

#
# Settings part
#
EXO_LIST = [
    #
    #  ContFut EXO must be first element of this list
    #     because ContFut EXO used by SmartEXOs we need to calculate it first
    {
        'name': 'ContFut',
        'class': EXOContinuousFut,
    },
    {
        'name': 'CollarBW',
        'class': EXOBrokenwingCollar,
    },
    {
        'name': 'VerticalSpread',
        'class': EXOVerticalSpread,
    },
    {
        'name': 'SmartexoIchimokuBearStraddle150Delta',
        'class': SmartexoIchimokuBearStraddle150Delta,
    },
    {
        'name': 'SmartEXOIchiBullishStraddle150DeltaExpHedgedNov22_2016',
        'class': SmartEXOIchiBullishStraddle150DeltaExpHedgedNov22_2016,
    },
    {
        'name': 'SmartEXO_Ichi_DeltaTargeting_Dec3_Bear_Bear_Spread',
        'class': SmartEXO_Ichi_DeltaTargeting_Dec3_Bear_Bear_Spread,
    },
    {
        'name': 'SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'class': SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread,
    },
    {
        'name': 'SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread',
        'class': SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread,
    },

]

# Alphas list (generic)
ALPHAS_GENERIC = ['alpha_exo']

# Custom alpha EXO list
ALPHAS_CUSTOM = [
    'cl_callspread',
    'cl_putspread',
    'cl_bearishcollarbw',
    'es_callspread',
    'es_putspread',
    'ng_callspread',
    'ng_putspread',
    'zn_callspread',
    'zn_putspread',
    'zc_callspread',
    'zc_putspread',
    'zs_callspread',
    'zs_putspread',
    'zw_callspread',
    'zw_putspread',
    'cl_smartexo_ichi_bearish_straddle_150delta',
    'cl_smartexo_ichi_bullish_straddle_150delta_exphedged_nov22_2016',
    'cl_contfut',
    'cl_smartexo_bi',
    'cl_smartexo_bull_bull'
]

# MongoDB credentials
#
MONGO_CONNSTR = 'mongodb://exowriter:qmWSy4K3@10.0.1.2/tmldb?authMechanism=SCRAM-SHA-1'
MONGO_EXO_DB = 'tmldb'

#
# SQL Server credentials
SQL_HOST = 'h9ggwlagd1.database.windows.net'
SQL_USER = 'modelread'
SQL_PASS = '4fSHRXwd4u'

#
# RabbitMQ credentials
RABBIT_HOST = 'localhost'
RABBIT_USER = 'guest'
RABBIT_PASSW = 'guest'
