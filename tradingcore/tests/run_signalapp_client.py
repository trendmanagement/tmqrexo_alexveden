from tradingcore.signalapp import SignalApp, APPCLASS_DATA
import time
from datetime import  datetime, time
from tradingcore.messages import *
from unittest.mock import MagicMock
from backtester.swarms.swarm import Swarm
app = SignalApp('asdasd', 'testclass')
#app = SignalApp('asdasd', 'EXO_ENGINE')

#app.send_to("ES", APPCLASS_DATA, {'msg': 'Test message', 'date': datetime.combine(datetime.now().date(), time(12, 45, 0))})
#app.send({'etst':'testse'})
app.send(MsgStatus("ERROR", 'Notifications test'))
print("{0}: Processed".format(datetime.now()))
#app.send(MsgEXOQuote("EXO_TEST", datetime.now()))
#app.send(MsgQuoteNotification("CL", datetime.now()))

mock_swm = MagicMock(spec=Swarm)
mock_swm.name = 'TEST_SWM'
mock_swm.exo_name = 'TEST_EXO'
mock_swm.instrument = 'TEST'
mock_swm.last_exposure = -1
mock_swm.last_prev_exposure = 2
mock_swm.last_rebalance_date = datetime.now()
mock_swm.last_date = datetime.now()


#msg_alpha_state = MsgAlphaState(mock_swm)
#app.send(msg_alpha_state)

#app.send(MsgAlphaSignal(msg_alpha_state, []))