from exobuilder.exo.transaction import Transaction
import copy
import warnings

class Position(object):
    def __init__(self):
        self._positions = {}
        self._realized_pnl = 0.0
        self._legs = {}

        self.transaction_mode = None
        self._last_trans_date = None

    @property
    def last_trans_date(self):
        return self._last_trans_date

    @property
    def netpositions(self):
        """
        List of opened net positions
        :return:
        """
        return self._positions

    @property
    def delta(self):
        """
        Return position delta
        Note: is position contains different instrument it will rise Excetion
        :return: position delta value
        """
        instrument = None
        delta = 0.0
        for asset, netposition in self.netpositions.items():
            if instrument is None:
                instrument = asset.instrument
            else:
                if instrument != asset.instrument:
                    raise Exception("Position contains multiple instruments, delta value is not applicable.\n Old instrument: {0} New instrument: {1}".format(instrument, asset.instrument))
            delta += asset.delta * netposition['qty']

        return delta


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
        """
        Returns list of transaction to close EXO position
        :return:
        """
        transactions = []
        for asset, netposition in self.netpositions.items():
            if netposition['qty'] != 0:
                transactions.append(Transaction(asset, asset.date, -netposition['qty'], asset.price, leg_name=netposition['leg_name']))

        return transactions

    def add_transaction_dict(self, trans_dict):
        """
        Add transaction as dictionary to speed up position construction (avoid DB calls)
        Used to construct position from MongoDB cached transactions
        :param trans_dict: transaction record dict as stored in Mongo
        :return: None (changes the position)
        """

        # Raise error if Transaction.add() method already called
        # It's not allowed to mix add_transaction_dict() and add() calls in single instance!
        if self.transaction_mode == 'T':
            raise Exception(
                "It's not allowed to mix add_transaction_dict() and add() calls in single Position instance!"
            )
        else:
            # Set Position instance to cached dictionary mode (works with Mongo result dicts)
            self.transaction_mode = "D"


        asset_hash = int(trans_dict['asset']['hash'])
        transaction_qty = trans_dict['qty']
        transation_usdvalue = trans_dict['usdvalue']

        if transaction_qty == 0:
            raise ValueError("Transaction Qty must be non-zero")

        self._last_trans_date = trans_dict['date']

        if asset_hash not in self._positions:
            self._positions[asset_hash] = {'qty': transaction_qty, 'value': transation_usdvalue}
        else:
            pdic = self._positions[asset_hash]
            pqty = pdic['qty']
            pval = pdic['value']

            if (pqty > 0 and transaction_qty < 0) or (pqty < 0 and transaction_qty > 0):
                # Closing or shrinking existing position
                # Calculate weighted usd value of opened position
                wavg_value = pval / pqty

                # Calculating realized PnL
                self._realized_pnl += wavg_value * transaction_qty - transation_usdvalue

                pdic['qty'] += transaction_qty
                pdic['value'] += wavg_value * transaction_qty
            else:
                pdic['qty'] += transaction_qty
                pdic['value'] += transation_usdvalue

            if pdic['qty'] == 0:
                # Delete closed positions
                del self._positions[asset_hash]


    def add(self, transaction):
        """Add new transaction to position"""

        # Raise error if Transaction.add_transaction_dict() method already called
        # It's not allowed to mix add_transaction_dict() and add() calls in single instance!
        if self.transaction_mode == 'D':
            raise Exception(
                "It's not allowed to mix add_transaction_dict() and add() calls in single Position instance!"
            )
        else:
            # Set Position instance to Transaction mode (works with Transaction class instances)
            self.transaction_mode = "T"

        if transaction.qty == 0:
            raise ValueError("Transaction Qty must be non-zero")

        self._last_trans_date = transaction.date

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

    def convert(self, datasource, date):
        """
        Converts restored position from transactions to normal position class
        Load asset instances from datasource and allow to analyse restored position as usual
        :param datasource: DataSource instance
        :param date: date of position analysis
        :return: None (converts internal position structure)
        """
        if len(self.netpositions) > 0 and self.transaction_mode != 'D':
            raise Exception(
                "Conversion is not allowed, current position instance must be initiated using add_transaction_dict()"
            )
        new_positions = {}
        for asset_hash, pos_dict in self.netpositions.items():
            asset_instance = datasource.get(int(asset_hash), date)
            new_positions[asset_instance] = pos_dict

        self._positions = new_positions

        # Set transaction mode to normal state
        # this will deny to call add_transaction_dict(), and allow us to use position pricing and add()
        self.transaction_mode = 'T'


    def as_dict(self):
        """
        Serialize Position to dictionary
        :return:
        """
        positions = {}

        for asset, pos in self.netpositions.items():
            positions[str(asset.__hash__())] = pos

        return {
            'positions': positions,
            '_realized_pnl': self._realized_pnl,
            '_last_trans_date': self.last_trans_date,
            }

    @staticmethod
    def from_dict(position_dict, datasource, date):
        """
        Initiate Position instance from dict (ex. from Mongo collection dict)
        :param position_dict: MongoDB collection dict
        :param datasource: Datasource to fetch all contracts instances
        :param date: current date
        :return: new Position class instance
        """
        p = Position()

        # Set transaction mode to normal state
        # this will deny to call add_transaction_dict(), and allow us to use position pricing and add()
        p.transaction_mode = 'T'

        positions = {}
        for asset_hash, pos_data in position_dict['positions'].items():
            asset_instance = datasource.get(int(asset_hash), date)
            positions[asset_instance] = pos_data

        # Filling position with data
        p._positions = positions
        if '_realized_pnl' in position_dict:
            p._realized_pnl = position_dict['_realized_pnl']
        else:
            p._realized_pnl = 0.0

        p._legs.clear()
        for asset, posdic in positions.items():
            if 'leg_name' in posdic and posdic['leg_name'] != '':
                p._legs[posdic['leg_name']] = asset

        if '_last_trans_date' in position_dict:
            p._last_trans_date = position_dict['_last_trans_date']

        return p

    @staticmethod
    def get_position_qty(exo_data, datasource):
        """
        Returns information about current EXO position structure, holdings names and qty
        :param exo_data: MongoDB collection dict
        :param datasource: datasource engine instance
        :return:
        """
        positions = {}
        position_dict = exo_data['position']
        for asset_hash, pos_data in position_dict['positions'].items():
            asset_info = datasource.get_info(int(asset_hash))
            positions[asset_info['name']] = {'qty': pos_data['qty'], 'asset': asset_info}

        return positions

    @property
    def usdvalue(self):
        """
        Calculates USD Value of opened position
        Used for PnL calculations in different price_whatif() scenarios
        :return:
        """
        usd_value = 0.0
        for asset, pos_data in self.netpositions.items():
            usd_value += pos_data['value']
        return usd_value


    @property
    def underlying(self):
        """
        Return instrument for single product position
        :return: Instrument instance
        """
        if self.transaction_mode == 'D':
            raise Exception(
                "You should call convert() for position restored from MongoDB dictionaries"
            )

        instrument = None
        for asset, pos_dict in self.netpositions.items():
            if instrument is not None:
                if asset.instrument != instrument:
                    raise Exception(
                        "Make sure that the position contains only single product. Multi-product pricing is not supported by default.")
            else:
                instrument = asset.instrument

        return instrument

    @property
    def underlying_price(self):
        """
        Return underlying price from position
        :return:
        """
        for asset, pos_dict in self.netpositions.items():
            if asset.contract_type == 'opt':
                return asset.underlying.price
            elif asset.contract_type == 'fut':
                return asset.price

        return 0.0

    def price_whatif(self, underlying_price=None, iv_change=0.0, days_to_expiration=None, riskfreerate=None):
        """
        What if analysis pricing depending on various conditions changes
        :param underlying_price: Price position with custom underlying price (if None, use current option price)
        :param iv_change: Price position with custom IV change (in percent points 0.01 - mean that IV rises OptionIV+1%, -0.05 - mean that IV drops OptionIV - 5%)
        :param days_to_expiration: Price position in different days_to_expiration values (0 - mean expired option payoff)
        :param riskfreerate: Set the risk free rate (if None - use the current RFR)
        :return: net position USD value and greeks on particular conditions
        """

        if self.transaction_mode == 'D':
            raise Exception(
                "You must call Position.convert() method before WhatIf pricing"
            )

        # Make sure that the position contains only single Product
        # Multi-product pricing is not supported by default
        instrument = None

        position_result = {'usdvalue': 0.0, 'delta': 0.0, 'whatif_positions': []}

        for asset, pos_dict in self.netpositions.items():
            if instrument is not None:
                if asset.instrument != instrument:
                    raise Exception("Make sure that the position contains only single product. Multi-product pricing is not supported by default.")
            else:
                instrument = asset.instrument

            whatif_data = asset.price_whatif(underlying_price=underlying_price,
                                             iv_change=iv_change,
                                             days_to_expiration=days_to_expiration,
                                             riskfreerate=riskfreerate)
            #
            # Add open price and qty information to asset position information
            #
            whatif_data['qty'] = pos_dict['qty']
            if pos_dict['qty'] == 0:
                whatif_data['open_price'] = 0.0
                whatif_data['pnl'] = 0.0
            else:
                whatif_data['open_price'] = pos_dict['value'] / pos_dict['qty'] / asset.pointvalue
                whatif_data['pnl'] = whatif_data['price'] * pos_dict['qty'] * asset.pointvalue - pos_dict['value']


            # Store information for every contract in position (what if priced info)
            position_result['whatif_positions'].append(whatif_data)

            # Calculate net position dollar value
            position_result['usdvalue'] += whatif_data['price'] * pos_dict['qty'] * asset.pointvalue
            position_result['delta'] += whatif_data['delta'] * pos_dict['qty']

        def sort_assets(a):
            asset = a['asset']

            if asset.startswith('F.'):
                return "0."+asset

            if asset.startswith('C.'):
                return "1." + asset

            if asset.startswith('P.'):
                return "2." + asset

            return asset

        # Sorting positions in next order: Fut -> Call -> Put
        position_result['whatif_positions'] = sorted(position_result['whatif_positions'], key=sort_assets)

        return position_result


    def __len__(self):
        return len(self.netpositions)


    def __str__(self):
        template = '{0:<25} | {1:<20} | {2:>10} | {3:>10} | {4:>10} | {5:>10} | {6:>10} | \n'
        result = 'Realized PnL: {0}\n'.format(self._realized_pnl)

        result += template.format('Leg', 'Asset', 'Qty', 'PnL', 'EntryPrice', 'CurrentPrice', 'Delta')

        for asset, pdic in self.netpositions.items():
            if pdic['qty'] == 0:
                continue
            result += template.format(pdic['leg_name'],
                                      asset.name,
                                      pdic['qty'],
                                      round(asset.pointvalue * asset.price * pdic['qty'] - pdic['value'], 2),
                                      round(pdic['value'] / asset.pointvalue / pdic['qty'], 2),
                                      round(asset.price, 2),
                                      round(asset.delta * pdic['qty'], 2))

        return result

