#
# Settings part
#


# EXO_LIST, INSTRUMENTS_LIST, ALPHAS_GENERIC moved to settings_exo.py file
# To avoid circular reference errors
# https://github.com/trendmanagement/tmqrexo_alexveden/issues/37
# EXO_LIST = []

# MongoDB credentials
#
MONGO_CONNSTR = 'mongodb://localhost'
MONGO_EXO_DB = 'tmldb_v2'

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
