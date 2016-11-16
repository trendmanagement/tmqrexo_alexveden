from exobuilder.exo.position import Position
from datetime import datetime
import warnings
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, HTML

class PayoffAnalyzer:
    def __init__(self, datasource):
        self.datasource = datasource
        self.position = None
        self.position_type = None
        self.position_name = None
        self.analysis_date = None

    def load_exo(self, exo_name, date=None):
        """
        Load EXO positions for further analysis
        :param exo_name: Name of EXO to analyze
        :param date: calculate EXO position on particular date (if None - return current position)
        :return: None
        """
        # Load EXO dict from EXO engine
        exo_data = self.datasource.exostorage.load_exo(exo_name)

        if exo_data is None:
            raise NameError("EXO data for {0} not found.".format(exo_name))

        # Calculate net position on particular date
        # Reconstruct position passing transactions from early days to current day
        pos_date = datetime.now() if date is None else date
        self.position = Position()

        for trans in exo_data['transactions']:
            if trans['date'] <= pos_date:
                self.position.add_transaction_dict(trans)

        # Convert position to normal state
        # We will load all assets information from DB
        # And this will allow us to use position pricing as well
        self.position.convert(self.datasource, pos_date)


        self.position_type = 'EXO'
        self.position_name = exo_name
        self.analysis_date = pos_date


    def load_campaign(self, campaign_name, date):
        """
        Load campaign net positions for further analysis
        :param campaign_name:
        :param date:
        :return:
        """
        # Load campaign positions

        # Calculate NET position on particular date

        # Store positions values for analysis
        self.position_type = 'Campaign'
        self.position_name = campaign_name
        pass

    def calc_payoff(self, strikes_to_analyze=10):
        """
        Calculates options positions payoff data for graphs (incl. PnL on expiration, current PnL, greeks)
        :return:
        """
        if self.position is None:
            raise Exception("You should run load_exo() or load_campaign() first")

        # Get actual price for underlying future contract
        current_price = self.position.underlying_price
        if current_price == 0.0:
            warnings.warn("Can't calculate payoff diagram for empty position")
            return None

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

            # Calculate payoff
            strike_payoff = {
                'strike': price_to_analyze,
                'current_payoff': whatif_data_current['usdvalue'] - pos_value,
                'current_delta': whatif_data_current['delta'],

                'expiration_payoff': whatif_data_exp['usdvalue'] - pos_value,
                'expiration_delta': whatif_data_exp['delta'],
            }
            payoffs.append(strike_payoff)

        dfresult = pd.DataFrame(payoffs)
        dfresult = dfresult.set_index('strike')
        return dfresult

    def position_info(self):
        """
        Returns net positions values (Qty, Greeks, Prices)
        :return:
        """
        if self.position is None:
            raise Exception("You should run load_exo() or load_campaign() first")

        pos_info = self.position.price_whatif()
        pos_info['opened_value'] = self.position.usdvalue
        pos_info['current_pnl'] = pos_info['usdvalue'] - self.position.usdvalue
        pos_info['current_ulprice'] = self.position.underlying_price
        return pos_info

    def plot(self, strikes_on_graph):

        dfpayoff = self.calc_payoff(strikes_to_analyze=strikes_on_graph)
        pos_info = self.position_info()

        f, (ax1, ax2) = plt.subplots(2, gridspec_kw={'height_ratios': [3, 1]});

        ax1.set_title('{0}: {1}'.format(self.position_type, self.position_name));
        dfpayoff['expiration_payoff'].plot(ax=ax1, label='At expiration');
        dfpayoff['current_payoff'].plot(ax=ax1, label='Current');
        ax1.axvline(pos_info['current_ulprice'], linestyle='--', c='grey', label='Current price');

        ax1.axhline(0, c='grey');
        ax1.legend()

        ax2.axvline(pos_info['current_ulprice'], linestyle='--', c='grey');
        dfpayoff['current_delta'].plot(ax=ax2, label='Delta');
        ax2.set_title('Delta');
        ax2.axhline(0, c='grey');

    def show_report(self):
        pos_info = self.position_info()

        print('Position analysis for {0}: {1}\n'.format(self.position_type, self.position_name))
        print('Analysis date: {0}'.format(self.analysis_date))
        print("PnL: {0:>10}".format(pos_info['current_pnl']))
        print("Delta: {0:>10}".format(pos_info['delta']))

        df = pd.DataFrame(pos_info['whatif_positions'])
        df = df.set_index('asset')
        df = df[['ulprice', 'open_price', 'price', 'qty', 'pnl', 'iv', 'delta', 'days_to_expiration', 'riskfreerate']]

        readable_col_names = {'ulprice': 'ULPrice',
                              'open_price': 'OpenPrice',
                              'price': 'CurrentPrice',
                              'qty': 'Qty',
                              'pnl': 'PnL',
                              'iv': 'IV',
                              'delta': 'Delta',
                              'days_to_expiration': 'To expiration',
                              'riskfreerate': 'RFR',
                              }

        df.rename(columns=readable_col_names, inplace=True)
        display(df)










