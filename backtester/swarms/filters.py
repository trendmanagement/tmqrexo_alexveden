import numpy as np
import pandas as pd


class SwarmFilter(object):
    @staticmethod
    def rolling_mean(avg_swarm_eqty, context):
        period = context['ma_period']
        ma = avg_swarm_eqty.rolling(period).mean()
        return avg_swarm_eqty > ma, {'values': ma, 'name': 'GF: Moving average ({0} periods)'.format(period)}


    @staticmethod
    def swingpoint_threshold(avg_swarm_eqty, context):
        period = context['period']
        down_factor = context['down_factor']
        up_factor = context['up_factor']

        vola = avg_swarm_eqty.diff(periods=period).abs().rolling(60).median()

        swing_point = pd.Series(np.nan, index=avg_swarm_eqty.index)
        swing_point_regime = pd.Series(0, index=avg_swarm_eqty.index)

        # Swing point bullish regime
        swing_switch = 1

        # Swing point start index
        sw_i = -1

        # Min/Max prices for swings
        sw_h_max = avg_swarm_eqty[0]
        sw_l_min = avg_swarm_eqty[0]

        for i in range(len(avg_swarm_eqty)):
            if i == 0:
                continue
            if np.isnan(avg_swarm_eqty[i]):
                continue
            if np.isnan(vola.values[i]):
                continue
            elif sw_i == -1 and vola.values[i] > 0:
                sw_h_max = sw_l_min = avg_swarm_eqty[i]
                sw_i = i

            if swing_switch == 1:
                #
                #  We have a bullish swing
                #
                sw_h_max = max(sw_h_max, avg_swarm_eqty[i])

                # Check for reversion
                if avg_swarm_eqty[i] <= sw_h_max - vola[sw_i] * down_factor:
                    # Reverse swing
                    swing_switch = -1
                    sw_l_min = avg_swarm_eqty.values[i]
                    sw_h_max = avg_swarm_eqty.values[i]
                    swing_point.values[i] = sw_l_min + vola[sw_i] * up_factor

                    sw_i = i
                else:
                    swing_point.values[i] = sw_h_max - vola[sw_i] * down_factor


            else:
                #
                #  We have a bearish swing
                #
                sw_l_min = min(sw_l_min, avg_swarm_eqty.values[i])

                # Check for reversion
                if avg_swarm_eqty.values[i] >= sw_l_min + vola[sw_i] * up_factor:
                    # Reverse swing
                    swing_switch = 1
                    sw_l_min = avg_swarm_eqty.values[i]
                    sw_h_max = avg_swarm_eqty.values[i]
                    sw_i = i
                    swing_point.values[i] = sw_h_max - vola[sw_i] * down_factor
                else:
                    swing_point.values[i] = sw_l_min + vola[sw_i] * up_factor

            swing_point_regime.values[i] = swing_switch

        return swing_point_regime == 1, {'values': swing_point,
                                         'name': 'GF: SwingPoint ({0} chg-periods, {1} up, {2} down)'.format(period, up_factor, down_factor)}