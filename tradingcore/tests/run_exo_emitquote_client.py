from tradingcore.signalapp import SignalApp, APPCLASS_EXO
from tradingcore.messages import *
from datetime import datetime

app = SignalApp('ES_CallSpread', APPCLASS_EXO)

app.send(MsgEXOQuote('ES_CallSpread', datetime.now()))