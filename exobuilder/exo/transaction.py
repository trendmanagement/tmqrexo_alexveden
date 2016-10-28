

class Transaction(object):
    def __init__(self, asset, date, qty, price=None, leg_name=''):
        self._asset = asset
        self._date = date
        self._qty = qty
        self._usdvalue = 0
        self._leg_name = leg_name

        if price is None:
            self._price = self._asset.price
        else:
            self._price = price

    @property
    def leg_name(self):
        return self._leg_name

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
    def delta(self):
        return self.asset.delta * self.qty

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

    def __eq__(self, other):
        if isinstance(other, Transaction):
            if self.asset == other.asset and self.date == other.date and self.qty == other.qty and self.price == other.price:
                return True

        return False

    def __str__(self):
        return "Leg: {0} / {1} x {2} Price: {3} Delta: {4}".format(self.leg_name, self.asset.name, self.qty, self.price, self.delta)
