import copy
from math import isnan, isfinite

class PlainMM:
    def __init__(self, acc_info):
        if 'size_factor' not in acc_info:
            raise ValueError("acc_info dictionary must contain 'size_factor' float value")

        self.size_factor = acc_info['size_factor']

        if self.size_factor <= 0:
            raise ValueError("acc_info 'size_factor' <= 0")

    @staticmethod
    def name():
        return 'plain'

    def get_positions(self, campaign):
        """
        Return round(campaign_positions * size_factor)
        :param campaign: campaign class instance
        :return: new positions_dict for current account
        """
        pos_dict = copy.deepcopy(campaign.positions)

        for asset in pos_dict.keys():
            pos_dict[asset]['qty'] = round(pos_dict[asset]['qty'])
            pos_dict[asset]['prev_qty'] = float('nan')
        return list(pos_dict.values())

    def get_position_at_date(self, campaign, date=None):
        """
        Returns the position of the account adjusted by acc qty at specific date
        :param campaign:
        :param date:
        :return:
        """
        return campaign.positions_at_date(date).adjust_and_round(self.size_factor)



class SmartCampaignMM:
    def __init__(self, acc_info):
        if 'smart_total_risk_percent' not in acc_info:
            raise ValueError("acc_info dictionary must contain 'smart_total_risk_percent' float value")

        if 'smart_equity' not in acc_info:
            raise ValueError("acc_info dictionary must contain 'smart_equity' float value")

        self.total_risk_percent = acc_info['smart_total_risk_percent']
        self.equity = acc_info['smart_equity']

        if self.total_risk_percent <= 0 or self.total_risk_percent >= 1:
            raise ValueError("acc_info 'smart_total_risk' <= 0 or >= 1")
        if self.equity <= 0 or not isfinite(self.equity):
            raise ValueError("acc_info 'smart_equity' <= 0 or NaN")


    @staticmethod
    def name():
        return 'smart'

    def get_positions(self, campaign):
        """
        Return round(campaign_positions * size_factor)
        :param campaign: campaign class instance
        :return: new positions_dict for current account
        """
        cmp_size_adj = self.get_camp_adj_size(campaign)

        pos_dict = copy.deepcopy(campaign.positions)
        for asset in pos_dict.keys():
            pos_dict[asset]['qty'] = round(pos_dict[asset]['qty'] * cmp_size_adj)
            pos_dict[asset]['prev_qty'] = float('nan')
        return list(pos_dict.values())

    def get_position_at_date(self, campaign, date=None):
        """
        Returns the position of the account adjusted by acc qty at specific date
        :param campaign:
        :param date:
        :return:
        """
        return campaign.positions_at_date(date).adjust_and_round(self.get_camp_adj_size(campaign))

    def get_camp_adj_size(self, campaign):
        if campaign.ctype != 'smart':
            raise ValueError("SmartCampaignMM is only compatible with SmartCampaigns")
        cmp_risk = campaign['campaign_risk']
        if cmp_risk <= 0 or not isfinite(cmp_risk):
            raise ValueError("{0}: 'campaign_risk' bad value {1}".format(campaign.name, cmp_risk))
        cmp_size_adj = self.equity * self.total_risk_percent / cmp_risk
        if cmp_size_adj <= 0 or not isfinite(cmp_size_adj):
            raise ValueError("{0} final campaign adjusted size bad value: {1}".format(campaign.name, cmp_size_adj))
        return cmp_size_adj


MM_CLASSES = {
    PlainMM.name(): PlainMM,
    SmartCampaignMM.name(): SmartCampaignMM,
}

