from exobuilder.exo.position import Position
import warnings
from exobuilder.exo.exoenginebase import ExoEngineBase
from datetime import datetime


class Campaign:
    def __init__(self, campaign_dict, datasource):
        self._dict = campaign_dict
        self._datasource = datasource
        self._legs = {}

        if 'alphas' in self._dict:
            for alpha_name, alpha_info in self._dict['alphas'].items():
                if 'leg_name' in alpha_info:
                    legs = self._legs.setdefault(alpha_info['leg_name'].lower(), [])
                    legs.append(alpha_name)
                else:
                    legs = self._legs.setdefault('', [])
                    legs.append(alpha_name)

    @property
    def name(self):
        return self._dict['name']

    @property
    def description(self):
        return self._dict['description']

    @property
    def dbid(self):
        return self._dict['_id']

    @property
    def legs(self):
        return sorted(list(self._legs.keys()))

    def as_dict(self):
        return self._dict

    @property
    def alphas(self):
        if 'alphas' not in self._dict:
            self._dict['alphas'] = {}
        return self._dict['alphas']

    def alphas_add(self, alpha_name, qty, leg_name=''):
        self.alphas[alpha_name] = {
            'qty': qty,
            'leg_name': leg_name
        }

        legs = self._legs.setdefault(leg_name.lower(), [])
        legs.append(alpha_name)


    def alphas_list(self, by_leg='*'):
        if by_leg == "*":
            return sorted(list(self.alphas.keys()))
        elif by_leg == '' or by_leg == None:
            return self._legs['']
        else:
            return self._legs[by_leg.lower()]

    def alphas_positions(self, date):
        """
        Returns list of alpha's exposures regarding campaign's qty
        :param date: if None - return current/last exposure, otherwize return exposure on particular date
        :return:
        """
        alpha_exposure = {}
        swarm_positions = self._datasource.exostorage.swarms_data(self.alphas.keys())
        if date is None:
            # If date is not defined return actual swarm exposures
            # Old behavior (for compatibility)
            for swarm_name, info_dict in swarm_positions.items():
                alpha_exposure[swarm_name] = {
                    'exposure': info_dict['last_exposure'] * self.alphas[swarm_name]['qty'],
                    'exo_name': info_dict['exo_name'],
                    }
        else:

            for swarm_name, info_dict in swarm_positions.items():
                seriesdf = info_dict['swarm_series']

                # Handle swarm indexing as Date and DateTime
                if date.date() in seriesdf.index:
                    # If index values represent EOD
                    exposure = seriesdf['exposure'].ix[date.date()]
                elif date in seriesdf.index:
                    # If index values are intraday timestamps
                    exposure = seriesdf['exposure'][date]
                else:
                    # Date is not found in swarm_series dataframe
                    exposure = 0.0
                    warnings.warn("Date ({0}) is not found in swarms series for {1}".format(date, swarm_name))

                alpha_exposure[swarm_name] = {
                    'exposure': exposure * self.alphas[swarm_name]['qty'],
                    'exo_name': info_dict['exo_name'],
                }

        return alpha_exposure

    def exo_positions(self, date):
        """
        Returns per EXO exposure of campaign
        :return:
        """
        exo_exposure = {}
        for k, v in self.alphas_positions(date).items():
            exp = exo_exposure.setdefault(v['exo_name'], {'exposure': 0.0})
            exo_exposure[v['exo_name']]['exposure'] = exp['exposure'] + v['exposure']
        return exo_exposure

    def positions_at_date(self, date=None):
        """
        Reconstruct campaign position at particular date
        :param pos_date: if None use last position
        :return:
        """
        exo_exposure = self.exo_positions(date)

        transactions = []

        pos_date = datetime.now() if date is None else date
        for exo_name, exp_dict in exo_exposure.items():
            # Skip zero-positions
            if exp_dict['exposure'] == 0:
                continue

            # Calculate position based on EXO transactions
            exo_data = self._datasource.exostorage.load_exo(exo_name)
            exo_df, exo_dict = self._datasource.exostorage.load_series(exo_name)

            if exo_data is None:
                raise NameError("EXO data for {0} not found.".format(exo_name))

            # Warn if something bad with EXO series
            ExoEngineBase.check_series_integrity(exo_name, exo_df, raise_exception=False)

            for trans in exo_data['transactions']:
                if trans['date'].date() <= pos_date.date():
                    if trans['qty'] == 0:
                        continue
                    trans['qty'] *= exp_dict['exposure']
                    trans['usdvalue'] *= exp_dict['exposure']
                    transactions.append(trans)
                else:
                    break

        # Sort transactions by date
        transactions = sorted(transactions, key=lambda k: k['date'])

        # Construct position
        position = Position()
        for t in transactions:
            position.add_transaction_dict(t)

        # Convert position to normal state
        # We will load all assets information from DB
        # And this will allow us to use position pricing as well
        position.convert(self._datasource, pos_date)
        return position

    @property
    def positions(self):
        """
        Returns net positions of campaign on last date
        :return:
        """
        net_positions = {}

        for exo_name, exo_exposure in self.exo_positions(date=None).items():
            # Load information about EXO positions
            exo_data = self._datasource.exostorage.load_exo(exo_name)

            if exo_data is not None:
                # Get EXO's assets positions
                exo_pos = Position.get_position_qty(exo_data, self._datasource)

                for assetname, pos_dict in exo_pos.items():
                    # Escape special MongoDB keys chars in key names
                    asset_name_safe = assetname.replace('.', '_').replace('$', '_')
                    position = net_positions.setdefault(asset_name_safe, {'asset': pos_dict['asset'], 'qty': 0.0, 'prev_qty': 0.0})

                    # Multiply EXO position by campaign exposure
                    position['qty'] += pos_dict['qty'] * exo_exposure['exposure']
                    position['prev_qty'] += float('nan')
            else:
                warnings.warn("EXO data not found for " + exo_name)

        return net_positions
