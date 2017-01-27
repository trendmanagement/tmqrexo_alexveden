"""
TODO: brief description of payoffs
"""
from exobuilder.exo.position import Position
from tradingcore.campaign import Campaign
from datetime import datetime
import warnings
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, HTML
import numpy as np
from exobuilder.exo.exoenginebase import ExoEngineBase

class PayoffAnalyzer:
    def __init__(self, datasource):
        self.datasource = datasource
        self.position = None
        self.position_type = None
        self.position_name = None
        self.analysis_date = None

    def load_transactions(self, transactions_list, analysis_date, position_name = ''):
        """
        Create payoff diagram analysis from transactions list
        :param transactions_list:
        :return:
        """
        self.position = Position()
        for trans in transactions_list:
            self.position.add(trans)

        self.position_type = 'TransList'
        self.position_name = position_name
        self.analysis_date = analysis_date

    def load_exo(self, exo_name, date=None):
        """
        Load EXO positions for further analysis
        :param exo_name: Name of EXO to analyze
        :param date: calculate EXO position on particular date (if None - return current position)
        :return: None
        """
        # Load EXO dict from EXO engine
        exo_data = self.datasource.exostorage.load_exo(exo_name)
        exo_df, exo_dict = self.datasource.exostorage.load_series(exo_name)

        if exo_data is None:
            raise NameError("EXO data for {0} not found.".format(exo_name))

        # Warn if something bad with EXO series
        ExoEngineBase.check_series_integrity(exo_name, exo_df, raise_exception=False)

        # Calculate net position on particular date
        # Reconstruct position passing transactions from early days to current day
        pos_date = datetime.now() if date is None else date
        self.position = Position()

        for trans in exo_data['transactions']:
            if trans['qty'] == 0:
                continue

            if trans['date'] <= pos_date:
                self.position.add_transaction_dict(trans)
            else:
                break


        if len(self.position.netpositions) == 0:
            if len(exo_data['transactions']) == 0:
                warnings.warn("EXO doesn't contain any transactions")
                return
            else:
                # Can't find any transactions on specific date
                warnings.warn(
                    "Can't find any transactions on specific date. First EXO transaction occured on {0}".format(
                        exo_data['transactions'][0]['date']))
                return

        # Convert position to normal state
        # We will load all assets information from DB
        # And this will allow us to use position pricing as well
        self.position.convert(self.datasource, pos_date)

        self.position_type = 'EXO'
        self.position_name = exo_name
        self.analysis_date = pos_date


    def load_campaign(self, campaign_name, date=None):
        """
        Load campaign net positions for further analysis
        :param campaign_name:
        :param date:
        :return:
        """
        # Load campaign positions
        campaign_dict = self.datasource.exostorage.campaign_load(campaign_name)
        if campaign_dict is None:
            warnings.warn("Campaign not found: " + campaign_name)
            return

        cmp = Campaign(campaign_dict, self.datasource)
        # Calculate campaign's net exo position on particular date
        pos_date = datetime.now() if date is None else date
        self.position = cmp.positions_at_date(date)

        # Store positions values for analysis
        self.position_type = 'Campaign'
        self.position_name = campaign_name
        self.analysis_date = pos_date

    def calc_payoff(self, strikes_to_analyze=10, iv_change=0.0, days_to_expiration=None):
        """
        Calculates options positions payoff data for graphs (incl. PnL on expiration, current PnL, greeks)
        :param strikes_to_analyze: number of strikes to show on Payoff graph
        :param iv_change: IV change in WhatIF scenario
        :param days_to_expiration: Days to expiration in WhatIF scenario
        :return:
        """
        if self.position is None:
            raise Exception("You should run load_exo() or load_campaign() first")

        # Get actual price for underlying future contract
        current_price = self.position.underlying_price

        # Calculate ATM strike for current price
        instrument = self.position.underlying
        atm_strike = instrument.get_atm_strike(current_price)
        strike_inc = instrument.optionstrikeincrement

        # Store position's opened value (used for PnL calculation)
        pos_value = self.position.usdvalue

        payoffs = []

        # Building option payoff diagram
        for soffset in range(-strikes_to_analyze, strikes_to_analyze, 1):
            price_to_analyze = atm_strike + soffset * strike_inc

            # Calculate current payoff of options position
            whatif_data_current = self.position.price_whatif(underlying_price=price_to_analyze)

            # Calculate options position value at expiration
            whatif_data_exp = self.position.price_whatif(underlying_price=price_to_analyze, days_to_expiration=0)

            # Calculate options position with WhatIF scenario included
            whatif_data_scenario = self.position.price_whatif(underlying_price=price_to_analyze,
                                                              iv_change=iv_change,
                                                              days_to_expiration=days_to_expiration)


            # Calculate payoff
            strike_payoff = {
                'strike': price_to_analyze,
                'current_payoff': whatif_data_current['usdvalue'] - pos_value,
                'current_delta': whatif_data_current['delta'],

                'expiration_payoff': whatif_data_exp['usdvalue'] - pos_value,
                'expiration_delta': whatif_data_exp['delta'],

                'scenario_payoff': whatif_data_scenario['usdvalue'] - pos_value,
                'scenario_delta':  whatif_data_scenario['delta'],
            }
            payoffs.append(strike_payoff)

        dfresult = pd.DataFrame(payoffs)
        dfresult = dfresult.set_index('strike')
        return dfresult

    def position_info(self, iv_change=0.0, days_to_expiration=None):
        """
        Returns net positions values (Qty, Greeks, Prices)
        :param iv_change: IV change in WhatIF scenario
        :param days_to_expiration: Days to expiration in WhatIF scenario
        :return:
        """
        if self.position is None:
            raise Exception("You should run load_exo() or load_campaign() first")

        pos_info = self.position.price_whatif(iv_change=iv_change, days_to_expiration=days_to_expiration)
        pos_info['opened_value'] = self.position.usdvalue
        pos_info['current_pnl'] = pos_info['usdvalue'] - self.position.usdvalue
        pos_info['current_ulprice'] = self.position.underlying_price
        return pos_info

    def plot(self, strikes_on_graph, iv_change, days_to_expiration):
        """
        Plot payoff diagram with WhatIF scenario
        :param strikes_to_analyze: number of strikes to show on Payoff graph
        :param iv_change: IV change in WhatIF scenario
        :param days_to_expiration: Days to expiration in WhatIF scenario
        :return:
        """
        if len(self.position.netpositions) == 0:
            warnings.warn("Can't calculate payoff diagram for empty position")
            return

        dfpayoff = self.calc_payoff(strikes_to_analyze=strikes_on_graph,
                                    iv_change=iv_change,
                                    days_to_expiration=days_to_expiration)
        pos_info = self.position_info()

        f, (ax1, ax2) = plt.subplots(2, gridspec_kw={'height_ratios': [3, 1]});

        ax1.set_title('{0}: {1}'.format(self.position_type, self.position_name));
        dfpayoff['expiration_payoff'].plot(ax=ax1, label='At expiration', lw=2, c='blue');
        dfpayoff['current_payoff'].plot(ax=ax1, label='Current', c='green');
        dfpayoff['scenario_payoff'].plot(ax=ax1, label='WhatIf', style='--', c='red');
        ax1.axvline(pos_info['current_ulprice'], linestyle='--', c='grey', label='Current price');

        ax1.axhline(0, c='grey');
        ax1.legend()

        ax2.axvline(pos_info['current_ulprice'], linestyle='--', c='grey');
        dfpayoff['expiration_delta'].plot(ax=ax2, c='blue', lw=2);
        dfpayoff['current_delta'].plot(ax=ax2, c='green');
        dfpayoff['scenario_delta'].plot(ax=ax2, style='--', c='red');
        ax2.set_title('Delta');
        ax2.axhline(0, c='grey');

        delta = dfpayoff['expiration_delta']

        ax2.set_ylim(delta.min() - 0.2, delta.max() + 0.2)

    def show_report(self, iv_change, days_to_expiration):
        if len(self.position.netpositions) == 0:
            warnings.warn("Can't calculate position report for empty position")
            return

        pos_info = self.position_info()

        print('Position analysis for {0}: {1}\n'.format(self.position_type, self.position_name))
        print('Analysis date: {0}'.format(self.analysis_date))
        print("PnL: {0:>10}".format(pos_info['current_pnl']))
        print("Delta: {0:>10}".format(pos_info['delta']))

        df = pd.DataFrame(pos_info['whatif_positions'])

        display(HTML(self._format_position_table(df)))

        whatif_pos_info = self.position_info(iv_change=iv_change, days_to_expiration=days_to_expiration)
        whatifdf = pd.DataFrame(whatif_pos_info['whatif_positions'])

        display(HTML(self._format_whatif_position_table(whatifdf, iv_change, days_to_expiration)))


    def _format_position_table(self, posdf):

        rows = ""

        table_template = """
        <div style="font-family:'Courier New', Courier, monospace;">
        <h4>Positions at {1}</h4>
        <table border="0" cellpadding="10" width="100%">
        <thead>
        <tr>
            <th style="text-align: center;">Asset</th>
            <th style="text-align: center;">OpenPrice</th>
            <th style="text-align: center;">CurrentPrice</th>
            <th style="text-align: center;">Qty</th>
            <th style="text-align: center;">PnL</th>
            <th style="text-align: center;">IV</th>
            <th style="text-align: center;">Delta</th>
            <th style="text-align: center;">ToExpiration</th>
            <th style="text-align: center;">RFR</th>
        </tr>
        </thead>
        {0}
        </table>
        </div>
        """

        row_template = '''
        <tr>
            <td>{asset}</td>
            <td style="text-align: right;">{open_price}</td>
            <td style="text-align: right;">{price}</td>
            <td style="text-align: right;">{qty}</td>
            <td style="text-align: right; {pnl_style}">${pnl:0.0f}</td>
            <td style="text-align: right;">{iv}</td>
            <td style="text-align: right;">{delta:0.2f}</td>
            <td style="text-align: right;">{days_to_expiration} days</td>
            <td style="text-align: right;">{riskfreerate}</td>
        </tr>
        '''
        def pnl_color(pnl):
            if pnl < 0:
                return 'color: #CC3327;'
            if pnl > 0:
                return 'color: #28CC52;'
            return ''

        instrument = self.position.underlying
        def format_price(asset, instrument, price):
            if asset.startswith('F.'):
                return round(price, len(str(instrument.ticksize)) - 2)
            elif asset.startswith('C.') or asset.startswith('P.'):
                return round(price, len(str(instrument.optionticksize)) - 2)
            return price

        def format_iv(iv):
            if np.isnan(iv):
                return ''
            return '{0:0.2f}%'.format(iv*100)


        for k, v in posdf.iterrows():
            values_dict = v.to_dict()
            values_dict['open_price'] = format_price(v['asset'], instrument, v['open_price'])
            values_dict['price'] = format_price(v['asset'], instrument, v['price'])
            values_dict['pnl_style'] = pnl_color(v['pnl'])
            values_dict['iv'] = format_iv(v['iv'])
            values_dict['riskfreerate'] = format_iv(v['riskfreerate'])


            rows += row_template.format(**values_dict)

        return table_template.format(rows, self.analysis_date)

    def _format_whatif_position_table(self, posdf, iv_change, days_to_expiration):

        rows = ""

        table_template = """
            <div style="font-family:'Courier New', Courier, monospace;">
            <h4>WhatIf scenario</h4>
            <p>
            IV change: {iv_change}
            </p>
            <p>
            Days to expiration: {days_to_expiration}
            </p>
            <table border="0" cellpadding="10" width="100%">
            <thead>
            <tr>
                <th style="text-align: center;">Asset</th>
                <th style="text-align: center;">OpenPrice</th>
                <th style="text-align: center;">CurrentPrice</th>
                <th style="text-align: center;">Qty</th>
                <th style="text-align: center;">PnL</th>
                <th style="text-align: center;">IV</th>
                <th style="text-align: center;">Delta</th>
                <th style="text-align: center;">ToExpiration</th>
                <th style="text-align: center;">RFR</th>
            </tr>
            </thead>
            {rows}
            </table>
            </div>
            """

        row_template = '''
            <tr>
                <td>{asset}</td>
                <td style="text-align: right;">{open_price}</td>
                <td style="text-align: right;">{price}</td>
                <td style="text-align: right;">{qty}</td>
                <td style="text-align: right; {pnl_style}">${pnl:0.0f}</td>
                <td style="text-align: right;">{iv}</td>
                <td style="text-align: right;">{delta:0.2f}</td>
                <td style="text-align: right;">{days_to_expiration} days</td>
                <td style="text-align: right;">{riskfreerate}</td>
            </tr>
            '''

        def pnl_color(pnl):
            if pnl < 0:
                return 'color: #CC3327;'
            if pnl > 0:
                return 'color: #28CC52;'
            return ''

        instrument = self.position.underlying

        def format_price(asset, instrument, price):
            if asset.startswith('F.'):
                return round(price, len(str(instrument.ticksize)) - 2)
            elif asset.startswith('C.') or asset.startswith('P.'):
                return round(price, len(str(instrument.optionticksize)) - 2)
            return price

        def format_iv(iv):
            if np.isnan(iv):
                return ''
            return '{0:0.2f}%'.format(iv * 100)

        for k, v in posdf.iterrows():
            values_dict = v.to_dict()
            values_dict['open_price'] = format_price(v['asset'], instrument, v['open_price'])
            values_dict['price'] = format_price(v['asset'], instrument, v['price'])
            values_dict['pnl_style'] = pnl_color(v['pnl'])
            values_dict['iv'] = format_iv(v['iv'])
            values_dict['riskfreerate'] = format_iv(v['riskfreerate'])

            rows += row_template.format(**values_dict)

        table_context = {
            'rows': rows,
            'iv_change': iv_change,
            'days_to_expiration': days_to_expiration,
        }

        return table_template.format(**table_context)











