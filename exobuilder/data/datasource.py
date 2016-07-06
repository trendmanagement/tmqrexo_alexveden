

class DataSourceBase(object):
    def __init__(self):
        pass

    def getdata(self, ticker, startdate, enddate):
        pass

    def __str__(self):
        return 'DataSourceBase'

