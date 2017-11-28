import holidays
from datetime import date


class TMQRHolidays(holidays.US):
    """
    Custom holidays for half-days in US exchanges
    """

    def _populate(self, year):
        # Populate base list of the holidays
        super()._populate(year)

        if year == 2017:
            self[date(year, 11, 24)] = 'Thanksgiving half-day'
