"""
TODO: brief description of filters.py
"""

import numpy as np
import pandas as pd
from backtester.common_algos import swingpoints


class SwarmFilter(object):
    @staticmethod
    def filter_equity(equity, gf_function, gf_context):

        is_picked, gf_data = gf_function(equity, gf_context)

        # Litte bit future referencing but without entry point bug
        # Unusable in production (real-time environments)
        eqty_chg = equity.shift(-1) - equity
        return eqty_chg[is_picked].cumsum().ffill(), gf_data


    @staticmethod
    def rolling_mean(avg_swarm_eqty, context):
        period = context['ma_period']
        ma = avg_swarm_eqty.rolling(period).mean()
        return avg_swarm_eqty > ma, {'values': ma, 'name': 'GF: Moving average ({0} periods)'.format(period)}


    @staticmethod
    def volatility_chandelier(avg_swarm_eqty, context):
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
                                         'input_equity': avg_swarm_eqty,
                                         'name': 'GF: SwingPoint ({0} chg-periods, {1} up, {2} down)'.format(period, up_factor, down_factor)}


    @staticmethod
    def swingpoint_daily(avg_swarm_eqty, context):
        down_factor = context['down_factor']
        up_factor = context['up_factor']


        spreadSeries = avg_swarm_eqty

        data = pd.DataFrame({'exo': spreadSeries, 'volume': pd.Series(0, index=spreadSeries.index) })
        sp_df = swingpoints(up_factor, down_factor, data)


        BULLISH = 1
        BEARISH = -1
        UNDEFINED = 0
        lastSWPHigh = np.inf  # intmax('int32');
        lastSWPLow = -np.inf  # intmin('int32');
        EPSILON = 0.000000000001

        nDays = len(sp_df)
        currentState = UNDEFINED
        nBase = 0  # nDays - length(spreadSeries);
        marketState = np.zeros(nDays, dtype=np.int8)  # zeros(1, nDays);

        sphIndicator = sp_df['sphIndicator'].values
        splIndicator = sp_df['splIndicator'].values
        sphLevel = sp_df['sphLevel'].values
        splLevel = sp_df['splLevel'].values

        for dd in range(1, nDays):
            if dd <= nBase:
                continue
            if sphIndicator[dd - nBase]:
                lastSWPHigh = sphLevel[dd - nBase]
            if splIndicator[dd - nBase]:
                lastSWPLow = splLevel[dd - nBase]

            if currentState == BULLISH:
                pass
                if (spreadSeries[dd - nBase] - lastSWPLow <= -EPSILON and
                                spreadSeries[dd - nBase - 1] - lastSWPLow > -EPSILON) \
                        or \
                        (lastSWPLow - lastSWPHigh >= EPSILON and
                                     spreadSeries[dd - nBase] - lastSWPHigh <= -EPSILON and
                                     spreadSeries[dd - nBase - 1] - lastSWPHigh > -EPSILON):
                    currentState = BEARISH

            elif currentState == BEARISH:
                if (spreadSeries[dd - nBase] - lastSWPHigh >= EPSILON and
                                spreadSeries[dd - nBase - 1] - lastSWPHigh < EPSILON) \
                        or \
                        (lastSWPLow - lastSWPHigh >= EPSILON and
                                     spreadSeries[dd - nBase] - lastSWPLow >= EPSILON and
                                     spreadSeries[dd - nBase - 1] - lastSWPLow < EPSILON):
                    currentState = BULLISH

            else:  # currentState == UNDEFINED
                if spreadSeries[dd] - lastSWPHigh >= EPSILON:
                    currentState = BULLISH
                if spreadSeries[dd] - lastSWPLow <= -EPSILON:
                    currentState = BEARISH

            marketState[dd] = currentState

        return pd.Series(marketState == BULLISH, index=spreadSeries.index, dtype=np.uint8), \
               {
                   'values': pd.Series(marketState, index=spreadSeries.index),
                    'input_equity': avg_swarm_eqty,
                    'name': 'GF: SwingPoint Daily ({0} up, {1} down)'.format(up_factor,
                                                                                              down_factor)
               }