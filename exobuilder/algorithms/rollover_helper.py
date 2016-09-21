





class RolloverHelper:
    def __init__(self, instrument, roll_regime_name='default'):
        self.instrument = instrument

        if self.instrument.name.upper() == "ZC":
            # Corn custom rollover options
            # corn spring	    0	0	1	0	1	0	1	0	0	0	0	0
            # corn winter	    0	0	0	0	0	0	0	0	1	0	0	1

            # corn speculative	1	1	1	0	1	0	1	0	1	0	0	1
            self.rollover_months = [1, 2, 3, 5, 7, 9, 12]
            self.days_before_expiration = 5

        else:
            # Default
            # Roll every month
            self.rollover_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            # Roll 2-days before expiration
            self.days_before_expiration = 2

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


