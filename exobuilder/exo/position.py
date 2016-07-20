from exobuilder.exo.transaction import Transaction
import copy

class Position(object):
    def __init__(self):
        self._positions = {}
        self._realized_pnl = 0.0

    @property
    def netpositions(self):
        """
        List of opened net positions
        :return:
        """
        return self._positions

    @property
    def pnl(self):
        """PnL of position"""
        pnl = 0.0
        for asset, netposition in self.netpositions.items():
            # calculate unrealized profit based on current price
            pnl += asset.pointvalue * asset.price * netposition['qty'] - netposition['value']
        return pnl + self._realized_pnl


    def add(self, transaction):
        """Add new transaction to position"""
        if transaction.asset not in self._positions:
            self._positions[transaction.asset] = {'qty': transaction.qty, 'value': transaction.usdvalue}
        else:
            pdic = self._positions[transaction.asset]

            pqty = pdic['qty']
            pval = pdic['value']

            if (pqty > 0 and transaction.qty < 0) or (pqty < 0 and transaction.qty > 0):
                # Closing or shrinking existing position

                # Calculate weighted usd value of opened position
                wavg_value = pval / pqty

                # Calculating realized PnL
                self._realized_pnl += wavg_value * transaction.qty - transaction.usdvalue

                pdic['qty'] += transaction.qty
                pdic['value'] += wavg_value * transaction.qty
            else:
                pdic['qty'] += transaction.qty
                pdic['value'] += transaction.usdvalue

            if pdic['qty'] == 0:
                # Delete closed positions
                del self._positions[transaction.asset]

    def as_dict(self):
        positions = {}

        for asset, pos in self.netpositions.items():
            positions[asset.__hash__()] = pos

        return {
            'positions': positions,
            '_realized_pnl': self._realized_pnl
            }

    @staticmethod
    def from_dict(position_dict, datasource):
        p = Position()

        positions = {}
        for asset_hash, pos_data in position_dict['positions'].items():
            asset_instance = datasource[asset_hash]

            positions[asset_instance] = pos_data

        # Filling position with data
        p._positions = positions
        p._realized_pnl = position_dict['_realized_pnl']

        return p

