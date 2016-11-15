from exobuilder.exo.position import Position
from datetime import datetime

class PayoffAnalyzer:
    def __init__(self, datasource):
        self.datasource = datasource
        self.position = None

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

        # Calculate NET position on particular date
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

        pass

    def calc_payoff(self):
        """
        Calculates options positions payoff data for graphs (incl. PnL on expiration, current PnL, greeks)
        :return:
        """
        pass

    def position_info(self):
        """
        Returns net positions values (Qty, Greeks, Prices)
        :return:
        """
        pass



