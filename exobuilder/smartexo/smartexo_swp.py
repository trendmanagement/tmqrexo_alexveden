from exobuilder.smartexo.smartexo_base import SmartEXOBase
from backtester.common_algos import swingpoints


class SmartEXOSwingpoint(SmartEXOBase):
    """
        Swingpoints regime base SmartEXO class
    """
    EXO_NAME = 'SmartEXOSwingpointBase'

    def __init__(self, symbol, direction, date, datasource, **kwargs):
        self.sphthreshold = kwargs.pop('sphthreshold', 2)
        self.splthreshold = kwargs.pop('splthreshold', 2)

        super().__init__(symbol, direction, date, datasource, **kwargs)

    def calculate_regime(self, date, exo_df):
        """
        Calculates Bull/Bear/Neutral areas based on Swingpoint zones

        param date: Current date time
        param price_series: price Pandas.Series

        Returns:
            -1 - for bearish zone
            0  - for neutral zone
            +1 - for bullish zone
            None - for unknown
        """
        swp_df = swingpoints(self.sphthreshold, self.splthreshold, exo_df)

        #
        # Rules calculation
        #

        bullish_reg = swp_df.price > swp_df.sphLevel
        bearish_reg = swp_df.price < swp_df.splLevel
        neutral_reg = (swp_df.price < swp_df.sphLevel) & (swp_df.price > swp_df.splLevel)

        def get_regime(date):
            if date not in neutral_reg.index:
                self.log("Date not found at {0}".format(date))
                return None

            if bullish_reg[date]:
                return 1
            elif bearish_reg[date]:
                return -1
            elif neutral_reg[date]:
                return 0
            return None

        regime = get_regime(date.date())
        self.log("SWP regime at {0}: {1}".format(date, regime))
        return regime
