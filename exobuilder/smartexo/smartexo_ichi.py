from exobuilder.smartexo.smartexo_base import SmartEXOBase


class SmartEXOIchi(SmartEXOBase):
    """
        Ichimoku regime base SmartEXO class
    """
    EXO_NAME = 'SmartEXOIchiBase'

    def __init__(self, symbol, direction, date, datasource, **kwargs):
        self.conversion_line_period = kwargs.pop('conversion_line_period', 9)  # subject of optimization 9
        self.base_line_period = kwargs.pop('base_line_period', 26)   # subject of optimization 26
        self.leading_spans_lookahead_period = kwargs.pop('leading_spans_lookahead_period', 26)  # subject of optimization 26
        self.leading_span_b_period = kwargs.pop('leading_span_b_period', 52) # subject of optimization 52

        super().__init__(symbol, direction, date, datasource, **kwargs)

    def calculate_regime(self, date, exo_df):
        price_series = exo_df['exo']

        conversion_line_period = self.conversion_line_period  # subject of optimization 9
        base_line_period = self.base_line_period  # subject of optimization 26
        leading_spans_lookahead_period = self.leading_spans_lookahead_period  # subject of optimization 26
        leading_span_b_period = self.leading_span_b_period  # subject of optimization 52

        conversion_line_high = price_series.rolling(window=conversion_line_period).max()
        conversion_line_low = price_series.rolling(window=conversion_line_period).min()
        conversion_line = (conversion_line_high + conversion_line_low) / 2

        base_line_high = price_series.rolling(window=base_line_period).max()
        base_line_low = price_series.rolling(window=base_line_period).min()
        base_line = (base_line_high + base_line_low) / 2

        leading_span_a = ((conversion_line + base_line) / 2).shift(leading_spans_lookahead_period)
        leading_span_b = ((price_series.rolling(window=leading_span_b_period).max() + price_series.rolling(
            window=leading_span_b_period).min()) / 2).shift(leading_spans_lookahead_period)

        #
        # Rules calculation
        #

        # Cloud top and bottom series are defined using leading span A and B
        cloud_top = leading_span_a.rolling(1).max()
        cloud_bottom = leading_span_a.rolling(1).min()

        rule_price_above_cloud_top = price_series > cloud_top
        rule_price_below_cloud_bottom = price_series < cloud_bottom
        rule_price_in_cloud = (price_series < cloud_top) & (price_series > cloud_bottom)

        def get_regime(date):
            if date not in rule_price_above_cloud_top.index:
                self.log("Date not found at {0}".format(date))
                return None

            if rule_price_above_cloud_top[date]:
                return 1
            elif rule_price_below_cloud_bottom[date]:
                return -1
            elif rule_price_in_cloud[date]:
                return 0
            return None

        regime = get_regime(date.date())
        self.log("Ichi regime at {0}: {1}".format(date, regime))
        return regime