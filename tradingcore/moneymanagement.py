class PlainMM:
    def __init__(self, acc_info):
        pass

    @staticmethod
    def name():
        return 'plain'

    def get_positions(self, campaign_positions):
        return campaign_positions


MM_CLASSES = {
    PlainMM.name(): PlainMM,
}
