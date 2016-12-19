from tradingcore.signalapp import SignalApp, APPCLASS_DATA
import time
from datetime import  datetime, time
from tradingcore.messages import *


app = SignalApp('asdasd', 'test')

#app.send_to("ES", APPCLASS_DATA, {'msg': 'Test message', 'date': datetime.combine(datetime.now().date(), time(12, 45, 0))})
#app.send({'etst':'testse'})
app.send(MsgStatus("TEST", 'Notifications test', notify=True))