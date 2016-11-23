"""
Main settings scripts for EXO and alpha management

List of settings:

1. ``INSTRUMENTS_LIST`` - list of products, used by online trading scripts
2. ``EXO_LIST`` - list of EXOs to build for every product in ``INSTRUMENTS_LIST``
3. ``ALPHAS_GENERIC`` - list of alphas to apply to every EXO in the system, represent module name (without .py extension) stored in ``scripts/alphas`` folder.
4. ``ALPHAS_CUSTOM`` - list of custom alpha folder with custom alphas modules, each record is an EXO name
5. ``MONGO_CONNSTR`` / ``MONGO_EXO_DB`` - global MongoDB credentials
6. ``SQL_HOST`` / ``SQL_USER`` / ``SQL_PASS`` - global TML SQL database credentials
7. ``RABBIT_HOST`` / ``RABBIT_USER`` / ``RABBIT_PASW`` - global RabbitMQ credentials for online notifications

"""

# Importing EXO code
from exobuilder.algorithms.exo_brokenwing import EXOBrokenwingCollar
from exobuilder.algorithms.exo_vertical_spread import EXOVerticalSpread
from exobuilder.algorithms.exo_continous_fut import EXOContinuousFut



#
# Instruments list
#
INSTRUMENTS_LIST = ['ES', 'CL', 'NG', 'ZN', 'ZS', 'ZW', 'ZC']

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
