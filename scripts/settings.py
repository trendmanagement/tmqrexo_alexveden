#
# Settings part
#


# EXO_LIST, INSTRUMENTS_LIST, ALPHAS_GENERIC moved to settings_exo.py file
# To avoid circular reference errors
# https://github.com/trendmanagement/tmqrexo_alexveden/issues/37
# EXO_LIST = []

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

STATUS_QUOTES_COLLECTION = 'status_quotes'

#
# TMQR Watchdog bot token
#
SLACK_TOKEN = "xoxb-118049439075-QjwhoyTBZlqLjJRmnjM0uT3B"
SLACK_CHANNEL = 'G3GPFV878'
