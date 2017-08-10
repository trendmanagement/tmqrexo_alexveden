# Importing EXO code
from exobuilder.algorithms.exo_brokenwing import EXOBrokenwingCollar
from exobuilder.algorithms.exo_vertical_spread import EXOVerticalSpread
from exobuilder.algorithms.exo_continous_fut import EXOContinuousFut
#from exobuilder.algorithms.smartexo_ichimoku_bear_straddle_150delta import SmartexoIchimokuBearStraddle150Delta
#from exobuilder.algorithms.smartexo_ichi_bullish_straddle_150delta_exphedged_nov22_2016 import SmartEXOIchiBullishStraddle150DeltaExpHedgedNov22_2016
#from exobuilder.algorithms.SmartEXO_Ichi_DeltaTargeting_Dec3_Bear_Bear_Spread import SmartEXO_Ichi_DeltaTargeting_Dec3_Bear_Bear_Spread
from exobuilder.algorithms.SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread import SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread
#from exobuilder.algorithms.SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread import SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread

from exobuilder.algorithms.smartexo_ichi_with_deltatargeting_bull_fence_v2 import SmartEXO_Ichi_Bullish_Fence
from exobuilder.algorithms.smartexo_ichi_with_deltatargeting_bear_fence_v2 import SmartEXO_Ichi_Bearish_Fence

#from exobuilder.algorithms.smartexo_bullish_ichi__dynamic_wrangle_1short_3long_jan11 import SmartEXO_Bullish_Ichi__Dynamic_Wrangle_1short_3Long_Jan11
#from exobuilder.algorithms.smartexo_ichi_dynamic_1short_3long_delta_bi_30_05_jan17 import SmartEXO_ichi_dynamic_1short_3long_delta_bi_30_05_jan17
#from exobuilder.algorithms.smartexo_ichi_dynamic_1short_3long_delta_bi_puts_30_05_Jan17 import SmartEXO_ichi_dynamic_1short_3long_delta_bi_puts_30_05_Jan17

from exobuilder.algorithms.SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly3X2_call_side import SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly3X2_call_side
from exobuilder.algorithms.SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly3X2_put_side import SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly3X2_put_side
from exobuilder.algorithms.SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly import SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly

#
# Instruments list
#
INSTRUMENTS_LIST = ['ES','CL','NG','ZN','ZS','ZW','ZC','6E','LBS','GC','CC','6J','ZL','6B','LE','SB','6C','6A','RB','HO',
                    'XAY', 'XAP', 'XAE', 'XAF', 'XAV', 'XAI', 'XAB', 'XAK', 'XAU']

# Alphas list (generic)
ALPHAS_GENERIC = ['alpha_exo']

# Custom alpha EXO list
# This setting is DEPRECATED
# ALPHAS_CUSTOM = []

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
    #{
    #    'name': 'SmartexoIchimokuBearStraddle150Delta',
    #    'class': SmartexoIchimokuBearStraddle150Delta,
    #},
    #{
    #    'name': 'SmartEXOIchiBullishStraddle150DeltaExpHedgedNov22_2016',
    #    'class': SmartEXOIchiBullishStraddle150DeltaExpHedgedNov22_2016,
    #},
    # {
    #     'name': 'SmartEXO_Ichi_DeltaTargeting_Dec3_Bear_Bear_Spread',
    #     'class': SmartEXO_Ichi_DeltaTargeting_Dec3_Bear_Bear_Spread,
    # },
    {
        'name': 'SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'class': SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread,
    },
    # {
    #     'name': 'SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread',
    #     'class': SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread,
    # },
    {
        'name': 'SmartEXO_Ichi_Class_Based_Bullish_Fence_Dec19',
        'class': SmartEXO_Ichi_Bullish_Fence,
    },
    {
        'name': 'SmartEXO_Ichi_Class_Based_Bearish_Fence_Dec19',
        'class': SmartEXO_Ichi_Bearish_Fence,
    },
    # {
    #     'name': 'SmartEXO_Bullish_Ichi__Dynamic_Wrangle_1short_3Long_Jan11',
    #     'class': SmartEXO_Bullish_Ichi__Dynamic_Wrangle_1short_3Long_Jan11,
    # },
    # {
    #     'name': 'SmartEXO_ichi_dynamic_1short_3long_delta_bi_30_05_jan17',
    #     'class': SmartEXO_ichi_dynamic_1short_3long_delta_bi_30_05_jan17,
    # },
    # {
    #     'name': 'SmartEXO_ichi_dynamic_1short_3long_delta_bi_puts_30_05_Jan17',
    #     'class': SmartEXO_ichi_dynamic_1short_3long_delta_bi_puts_30_05_Jan17,
    # },
    {
        'name': 'SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly3X2_call_side',
        'class': SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly3X2_call_side,
    },
    {
        'name': 'SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly3X2_put_side',
        'class': SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly3X2_put_side,
    },
    {
        'name': 'SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly',
        'class': SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly,
    },

]



