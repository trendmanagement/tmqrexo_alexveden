from tradingcore.signalapp import SignalApp
import time
from datetime import datetime

app = SignalApp('*', 'testclass')

def callback(appname, appclass, data):
    print(appname + '.' + appclass)
    #print(data)
    print("Before sleep: {0}".format(datetime.now()))
    print('Waiting')
    time.sleep(10)
    print("After sleep: {0}".format(datetime.now()))
    print("Done")

print("Listening")

app.listen(callback)