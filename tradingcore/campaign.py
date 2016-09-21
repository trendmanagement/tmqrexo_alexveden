from exobuilder.exo.position import Position


class Campaign:
    def __init__(self, campaign_dict, mongodb, datasource):
        self._dict = campaign_dict
        self._db = mongodb
        self._datasource = datasource
        self._legs = {}

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

    @property
    def alphas(self):
        return self._dict['alphas']

    def alphas_add(self, alpha_name, qty, leg_name=''):
        self.alphas[alpha_name] = {
            'qty': qty,
            'leg_name': leg_name
        }

        legs = self._legs.setdefault(leg_name.lower(), [])
        legs.append(alpha_name)
        pass

    def alphas_list(self, by_leg='*'):
        if by_leg == "*":
            return sorted(list(self.alphas.keys()))
        elif by_leg == '' or by_leg == None:
            return self._legs['']
        else:
            return self._legs[by_leg.lower()]

    @property
    def alphas_positions(self):
        """
        Returns list of alpha's exposures regarding campaign's qty
        :return:
        """
        alpha_exposure = {}
        for swarm_name, info_dict in self._datasource.exostorage.swarms_positions(self.alphas.keys()).items():
            alpha_exposure[swarm_name] = {
                'exposure': info_dict['exposure'] * self.alphas[swarm_name]['qty'],
                'exo_name': info_dict['exo_name'],
                }
        return alpha_exposure

    @property
    def exo_positions(self):
        """
        Returns per EXO exposure of campaign
        :return:
        """
        exo_exposure = {}
        for k, v in self.alphas_positions.items():
            exp = exo_exposure.setdefault(v['exo_name'], 0.0)
            exo_exposure[v['exo_name']] = exp + v['exposure']
        return exo_exposure


    @property
    def positions(self):
        """
        Returns net positions of campaign
        :return:
        """
        net_positions = {}

        for exo_name, exo_exposure in self.exo_positions.items():
            # Load information about EXO positions
            exo_data = self._datasource.exostorage.load_exo(exo_name)

            if exo_data is not None:
                # Get EXO's assets positions
                exo_pos = Position.get_info(exo_data['position'], self._datasource)

                for assetname, pos_dict in exo_pos.items():
                    position = net_positions.setdefault(assetname, {'asset': pos_dict['asset'], 'qty': 0.0})

                    # Multiply EXO position by campaign exposure
                    position['qty'] += pos_dict['qty'] * exo_exposure

        return net_positions
