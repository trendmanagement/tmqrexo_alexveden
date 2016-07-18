

class Transaction(object):
    def __init__(self, asset, date, qty, price):
        self._asset = asset
        self._date = date
        self._qty = qty
        self._price = price

    @property
    def asset(self):
        return self._asset

    @property
    def date(self):
        return self._date

    @property
    def qty(self):
        return self._qty

    @property
    def price(self):
        return self._price

    @property
    def usdvalue(self):
        return self._price * self._qty * self._asset.pointvalue