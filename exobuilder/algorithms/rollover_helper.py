import re


class RolloverHelper:
    def __init__(self, instrument, **kwargs):
        self.instrument = instrument

        re_include = kwargs.get('option_code_include', [])

        self.re_option_code_include = []

        for pattern in re_include:
            self.re_option_code_include.append(re.compile(pattern))

        # Default
        # Roll every month
        self.rollover_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        # Roll 2-days before expiration
        self.days_before_expiration = 2

        if self.instrument.name.upper() == "ZC":
            # Corn custom rollover options
            # corn spring	    0	0	1	0	1	0	1	0	0	0	0	0
            # corn winter	    0	0	0	0	0	0	0	0	1	0	0	1

            # corn speculative	1	1	1	0	1	0	1	0	1	0	0	1
            self.rollover_months = [1, 2, 3, 5, 7, 9, 12]
            self.days_before_expiration = 5

        if self.instrument.name.upper() == "ZW":
            """Option	Future
            Jan	Mar
            Feb	Mar
            Mar	Mar
            Apr	May
            May	May
            Jun	Jun
            Jul	Jul
            Aug	Sep
            Sep	Sep
            Oct	Dec
            Nov	Dec
            Dec	Dec
            """
            self.rollover_months = [3, 5, 6, 7, 9, 12]
            self.days_before_expiration = 5

        if self.instrument.name.upper() == "ZS":
            """
            Soy

            Option	Future

            Jan	Jan
            Feb	Mar
            Mar	Mar
            Apr	May
            May	May
            Jun	Jul
            Jul	Jul
            Aug	Aug
            Sep	Sep
            Oct	Nov
            Nov	Nov
            Dec	Jan
            """
            self.rollover_months = [1, 3, 5, 7, 8, 9, 11]
            self.days_before_expiration = 5

        if self.instrument.name.upper() == "CC":
            """
            Cocoa

            Option	Future

            Jan	Mar
            Feb	Mar
            Mar	Mar
            Apr	May
            May	May
            Jun	Jul
            Jul	Jul
            Aug	Sep
            Sep	Sep
            Oct	Dec
            Nov	Dec
            Dec	Dec
            """
            self.rollover_months = [3, 5, 7, 9, 12]
            self.days_before_expiration = 5

        if self.instrument.name.upper() == "LE":
            """
            Live Cattle
            """
            self.rollover_months = [2, 4, 6, 8, 10, 12]
            self.days_before_expiration = 5

        if self.instrument.name.upper() == "SB":
            """
            Sugar No. 11
            """
            self.rollover_months = [3, 5, 7, 10]
            self.days_before_expiration = 5

        if self.instrument.name.upper() == "LBS":
            """
            Lumber

            Option	Future

            Jan	Jan
            Feb	Mar
            Mar	Mar
            Apr	May
            May	May
            Jun	Jul
            Jul	Jul
            Aug	Sep
            Sep	Sep
            Oct	Nov
            Nov	Nov
            Dec	Jan
            """
            self.rollover_months = [1, 3, 5, 7, 9, 11]
            self.days_before_expiration = 5

        if self.instrument.name.upper() == "ES":
            self.rollover_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            self.days_before_expiration = 2
            if len(self.re_option_code_include) == 0:
                self.re_option_code_include = [
                    re.compile('^EW$'),       # Matches end-of-month option
                    re.compile('^$'),         # Matches '' empty option code
                ]

        if self.instrument.name.upper() == "GC":
            """
            Gold
            """
            self.rollover_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            self.days_before_expiration = 5

        if self.instrument.name.upper() == "6E":
            """
            https://github.com/trendmanagement/tmqrexo_alexveden/issues/134
            @steve
            On Feb 22 2017 CME introduced monthly futures on all of their FX products.
            The options are only on the quarterly futures.
            So the roll schedule for CME FX products will be monthly for the options on the quarterly futures.
            """
            self.rollover_months = [3, 6, 9, 12]
            self.days_before_expiration = 2
            if len(self.re_option_code_include) == 0:
                self.re_option_code_include = [
                    re.compile('^EUU$'),       # Matches end-of-month option
                    re.compile('^$'),          # Matches '' empty option code
                ]

        if self.instrument.name.upper() == "6J":
            """
            https://github.com/trendmanagement/tmqrexo_alexveden/issues/134
            @steve
            On Feb 22 2017 CME introduced monthly futures on all of their FX products.
            The options are only on the quarterly futures.
            So the roll schedule for CME FX products will be monthly for the options on the quarterly futures.
            """
            self.rollover_months = [3, 6, 9, 12]
            self.days_before_expiration = 2
            if len(self.re_option_code_include) == 0:
                self.re_option_code_include = [
                    re.compile('^JPU$'),       # Matches end-of-month option
                    re.compile('^$'),          # Matches '' empty option code
                ]

        if self.instrument.name.upper() == "6B":
            """
            https://github.com/trendmanagement/tmqrexo_alexveden/issues/134
            @steve
            On Feb 22 2017 CME introduced monthly futures on all of their FX products.
            The options are only on the quarterly futures.
            So the roll schedule for CME FX products will be monthly for the options on the quarterly futures.
            """
            self.rollover_months = [3, 6, 9, 12]
            self.days_before_expiration = 2
            if len(self.re_option_code_include) == 0:
                self.re_option_code_include = [
                    re.compile('^GBU$'),       # Matches end-of-month option
                    re.compile('^$'),          # Matches '' empty option code
                ]



    def _get_recent_option_chain(self, fut):
        """
        Returns most recent option contract for future contract
        :param fut:
        :return:
        """
        if fut is None:
            return None

        for opt in fut.options:
            if opt.to_expiration_days > self.days_before_expiration:
                if self.check_option_code_included(opt.option_code):
                    return opt
        return None

    def _get_next_future(self, start_idx=-1):
        """
        Returns most recent (not expired) future contract
        :param start_idx:
        :return:
        """
        for i in range(start_idx+1, len(self.instrument.futures)):
            f = self.instrument.futures[i]
            if f.to_expiration_days > self.days_before_expiration and f.expiration.month in self.rollover_months:
                return f, i

        return None, -1

    def is_rollover(self, asset):
        if asset.to_expiration_days <= self.days_before_expiration:
            return True
        return False

    def check_option_code_included(self, option_code):
        """
        Checks regular expressions passed by 'option_code_include' kwarg in constructor,
        if option code doesn't match just ignore, if 'option_code_include' always return True
        :return:
        """
        if len(self.re_option_code_include) == 0:
            return True

        for re_include in self.re_option_code_include:
            if re_include.fullmatch(option_code) is not None:
                return True

        return False



    def get_active_chains(self):
        fut, fut_idx = self._get_next_future()

        # Future contract not found
        if fut is None:
            return None, None

        # Getting most recent option contract
        opt_chain = self._get_recent_option_chain(fut)

        # if option almost expired
        if opt_chain is None:
            # Getting next futures series
            fut, fut_idx = self._get_next_future(start_idx=fut_idx)
            # Getting next futures series options
            opt_chain = self._get_recent_option_chain(fut)

            # Option chains not found (suspect that options chains not exist)
            if opt_chain is None:
                # Just return most recent futures without options
                return self._get_next_future()[0], None

        return fut, opt_chain


