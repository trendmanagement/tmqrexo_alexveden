from exobuilder.exo.transaction import Transaction


class Position(object):
    def __init__(self):
        self._transactions = []
        self._is_closed = False

    @property
    def netpositions(self):
        """
        List of opened net positions
        :return:
        """
        netpositions = {}
        for t in self._transactions:
            if t.asset in netpositions:
                netpositions[t.asset]['qty'] += t.qty
                netpositions[t.asset]['value'] += -t.usdvalue
            else:
                netpositions[t.asset] = {'qty': t.qty, 'value': -t.usdvalue}
        return netpositions

    @property
    def pnl(self):
        """PnL of position"""
        pnl = 0.0
        for asset, netposition in self.netpositions.items():
            if netposition['qty'] == 0:
                # This is closed position add its realized profit
                pnl += netposition['value']
            else:
                # This is opened position, calculate unrealized profit based on current price
                pnl += netposition['value'] + asset.pointvalue * asset.price * netposition['qty']
        return pnl


    @property
    def transactions(self):
        """List of transactions for position"""
        return self._transactions

    def close(self, date):
        """Close all net positions inside portfolio"""
        for asset, netposition in self.netpositions.items():
            if netposition['qty'] != 0:
                self.add(asset, date, -netposition['qty'], asset.price)

        self._is_closed = True

    def add(self, asset, date, qty, price):
        """Add new transaction to position"""
        self._transactions.append(Transaction(asset, date, qty, price))

    def add_transaction(self, transaction):
        """Add new transaction to position"""
        self._transactions.append(transaction)

    @property
    def is_closed(self):
        return self._is_closed