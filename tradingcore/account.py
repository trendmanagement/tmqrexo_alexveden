

class Account:
    def __init__(self, acc_dict, campaign, mmclass):
        self._dict = acc_dict
        self.campaign = campaign
        self.mmclass = mmclass

    @property
    def name(self):
        return self._dict['name']

    @property
    def client_name(self):
        return self._dict['client_name']

    @property
    def dbid(self):
        return self._dict['_id']

    def positions(self):
        return self.mmclass.get_positions(self.campaign.positions)

    def as_dict(self):
        self._dict['campaign_name'] = self.campaign.name
        self._dict['mmclass_name'] = self.mmclass.name()
        return self._dict


