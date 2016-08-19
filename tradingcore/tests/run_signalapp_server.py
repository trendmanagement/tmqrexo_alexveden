from tradingcore.signalapp import SignalApp


app = SignalApp('*', 'testclass')

def callback(appname, appclass, data):
    print(appname + '.' + appclass)

    print(data)

print("Listening")

app.listen(callback)