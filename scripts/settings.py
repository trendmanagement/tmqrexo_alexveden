# Importing EXO code
from exobuilder.algorithms.exo_brokenwing import EXOBrokenwingCollar
from exobuilder.algorithms.exo_vertical_spread import EXOVerticalSpread
from exobuilder.algorithms.exo_continous_fut import EXOContinuousFut



#
# Instruments list
#
INSTRUMENTS_LIST = ['ES', 'CL', 'NG', 'ZN', 'ZS', 'ZW']

#
# Settings part
#
EXO_LIST = [
    {
        'name': 'CollarBW',
        'class': EXOBrokenwingCollar,
    },
    {
        'name': 'VerticalSpread',
        'class': EXOVerticalSpread,
    },
    {
        'name': 'ContFut',
        'class': EXOContinuousFut,
    },

]

# Alphas list (generic)
ALPHAS_GENERIC = ['alpha_bollingerbands',
                  'alpha_ichimoku',
                  'alpha_macross',
                  'alpha_pointnfigure',
                  'alpha_renko_noexit',
                  'alpha_swingpoint',
                  'alpha_volcompression'
                  ]

# Custom alpha EXO list
ALPHAS_CUSTOM = [
    'cl_callspread',
    'cl_putspread',
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