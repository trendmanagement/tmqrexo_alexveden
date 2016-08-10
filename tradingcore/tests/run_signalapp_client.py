from tradingcore.signalapp import SignalApp
import time
from datetime import  datetime

app = SignalApp('test', 'testclass')

while True:
    app.send("test", 'testclass', {'msg': 'Test message', 'date': datetime.now()})
    time.sleep(1)