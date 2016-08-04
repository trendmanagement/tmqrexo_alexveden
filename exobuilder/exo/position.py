from exobuilder.exo.transaction import Transaction
import copy

class Position(object):
    def __init__(self):
        self._positions = {}
        self._realized_pnl = 0.0
        self._legs = {}

    @property
    def netpositions(self):
        """
        List of opened net positions
        :return:
        """
        return self._positions

    @property
    def legs(self):
        return self._legs

    @property
    def pnl(self):
        """PnL of position"""
        pnl = 0.0
        for asset, netposition in self.netpositions.items():
            # calculate unrealized profit based on current price
            pnl += asset.pointvalue * asset.price * netposition['qty'] - netposition['value']
        return pnl + self._realized_pnl

    def close_all_translist(self):
        transactions = []
        for asset, netposition in self.netpositions.items():
            transactions.append(Transaction(asset, asset.date, -netposition['qty'], asset.price, leg_name=netposition['leg_name']))

        return transactions


    def add(self, transaction):
        """Add new transaction to position"""
        if transaction.asset not in self._positions:
            self._positions[transaction.asset] = {'qty': transaction.qty, 'value': transaction.usdvalue, 'leg_name': transaction.leg_name}
            if transaction.leg_name != '':
                if transaction.leg_name in self._legs:
                    raise NameError("Leg with name '{0}' already exists. Existing asset: {1} New asset: {2}".format(transaction.leg_name, self._legs[transaction.leg_name], transaction.asset))
                self._legs[transaction.leg_name] = transaction.asset
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
                if pdic['leg_name'] != '' and pdic['leg_name'] in self._legs:
                    del self.legs[pdic['leg_name']]

    def as_dict(self):
        positions = {}

        for asset, pos in self.netpositions.items():
            positions[str(asset.__hash__())] = pos

        return {
            'positions': positions,
            '_realized_pnl': self._realized_pnl
            }

    @staticmethod
    def from_dict(position_dict, datasource, date):
        p = Position()

        positions = {}
        for asset_hash, pos_data in position_dict['positions'].items():
            asset_instance = datasource.get(int(asset_hash), date)

            positions[asset_instance] = pos_data

        # Filling position with data
        p._positions = positions
        p._realized_pnl = position_dict['_realized_pnl']

        p._legs.clear()
        for asset, posdic in positions.items():
            if 'leg_name' in posdic and posdic['leg_name'] != '':
                p._legs[posdic['leg_name']] = asset


        return p

    def __len__(self):
        return len(self.netpositions)


    def __str__(self):
        template = '{0:<25} | {1:<20} | {2:>10} | {3:>10} | {4:>10} | {5:>10} | \n'
        result = 'Realized PnL: {0}\n'.format(self._realized_pnl)

        result += template.format('Leg', 'Asset', 'Qty', 'PnL', 'EntryPrice', 'CurrentPrice')

        for asset, pdic in self.netpositions.items():
            result += template.format(pdic['leg_name'],
                                      asset.name,
                                      pdic['qty'],
                                      round(asset.pointvalue * asset.price * pdic['qty'] - pdic['value'], 2),
                                      round(pdic['value'] / asset.pointvalue / pdic['qty'], 2),
                                      round(asset.price, 2))

        return result

