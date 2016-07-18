from exobuilder.exo.position import Position
from exobuilder.exo.transaction import Transaction


class ExoEngineBase(object):
    def __init__(self, date, datasource):
        self._positions = []
        self._date = date
        self._datasource = datasource

    def is_rollover(self):
        pass

    def process_rollover(self):
        """
        Typically we should only close old position on rollover day
        :return:
        """
        pass

    def process_day(self):
        """
        Main EXO's position management method
        :return: list of Transactions to process
        """
        pass

    def _calculate(self):
        """
        Main internal method to manage EXO data
        :return:
        """

        old_pos = self.position
        old_pnl = 0.0
        if old_pos is not None:
            old_pnl = old_pos.pnl

        # Proto-code
        if self.is_rollover():
            self.process_rollover()

            # Process closed position PnL to change EXO price for current day
            # ???

        # Processing new day
        new_transactions = self.process_day()

        if new_transactions is not None and len(new_transactions) > 0:
            if self.position is None:
                # Create new position
                p = Position()
                for t in new_transactions:
                    p.add_transaction(t)

                # Append new position to EXO
                self._positions.append(p)
            else:
                p = self.position
                for t in new_transactions:
                    p.add_transaction(t)

        pnl = self.position.pnl

        pnl_diff = pnl - old_pnl

        # Append pnl_diff to EXO series values
        #? ?????

        # Save EXO state to DB
        self.save()







    def _save(self):
        """
        Save the EXO data to DB
        :return:
        """
        pass

    def _load(self):
        """
        Load EXO data from DB
        :return:
        """
        pass

    @property
    def position(self):
        """
        Returns current opened position of EXO engine
        If position is closed return None
        :return: None or Position()
        """
        pass

    @property
    def price_series(self):
        """
        Returns EXO price series values (before current date)
        :return:
        """
        pass

    @property
    def date(self):
        return self._date

    @property
    def datasource(self):
        return self._datasource