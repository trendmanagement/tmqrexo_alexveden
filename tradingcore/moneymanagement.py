import copy

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

    def get_positions(self, campaign_positions):
        """
        Return round(campaign_positions * size_factor)
        :param campaign_positions: net campaign positions
        :return: new positions_dict for current account
        """
        pos_dict = copy.deepcopy(campaign_positions)
        for asset in pos_dict.keys():
            if pos_dict[asset]['qty'] == 0:
                continue
            pos_dict[asset]['qty'] = round(pos_dict[asset]['qty'] * self.size_factor)
            pos_dict[asset]['prev_qty'] = float('nan')
        return list(pos_dict.values())


MM_CLASSES = {
    PlainMM.name(): PlainMM,
}

