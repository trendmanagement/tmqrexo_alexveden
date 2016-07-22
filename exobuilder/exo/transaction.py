

class Transaction(object):
    def __init__(self, asset, date, qty, price):
        self._asset = asset
        self._date = date
        self._qty = qty
        self._price = price
        self._usdvalue = 0

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
        if self._usdvalue == 0:
            self._usdvalue = self._price * self._qty * self._asset.pointvalue

        return self._usdvalue

    def as_dict(self):
        return {
            'date': self.date,
            'qty': self.qty,
            'price': self.price,
            'asset': self.asset.as_dict(),
            'usdvalue': self.usdvalue,
            }
