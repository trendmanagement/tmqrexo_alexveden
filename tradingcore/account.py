import warnings

class Account:
    def __init__(self, acc_dict, campaign, mmclass, isactive=True):
        self.name = acc_dict['name']
        self.client_name = acc_dict['client_name']
        self.info = acc_dict['info']
        self.campaign = campaign
        self.mmclass = mmclass
        self.isactive = isactive
        if 'instruments' not in acc_dict or len(acc_dict['instruments']) == 0:
            warnings.warn("'instruments' key is not found or empty in accounts dict")
            self.instruments = []
        else:
            self.instruments = acc_dict['instruments']


    @property
    def positions(self):
        return self.mmclass.get_positions(self.campaign.positions)

    def as_dict(self):
        result = {}
        result['campaign_name'] = self.campaign.name
        result['mmclass_name'] = self.mmclass.name()
        result['name'] = self.name
        result['client_name'] = self.client_name
        result['info'] = self.info
        result['isactive'] = self.isactive
        result['instruments'] = self.instruments
        return result

