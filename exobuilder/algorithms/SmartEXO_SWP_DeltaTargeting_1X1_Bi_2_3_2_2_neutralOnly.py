import importlib
import logging

from exobuilder.exo.transaction import Transaction

importlib.reload(logging);

from exobuilder.smartexo.smartexo_swp import SmartEXOSwingpoint
from bdateutil import relativedelta
import holidays


class SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly(SmartEXOSwingpoint):

    # Change the EXO name to reflect SmartEXO behavior
    EXO_NAME = 'SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly'

    # select instruments list for SMART EXO calculation
    ASSET_LIST = None

    def __init__(self, symbol, direction, date, datasource, **kwargs):
        super().__init__(symbol, direction, date, datasource,
                         sphthreshold=2,
                         splthreshold=2,
                         )

    @staticmethod
    def new_position_bullish_zone(date, fut, opt_chain):
        """
        opt_chain.get_by_delta(delta_value) help:

        Search option contract by delta value:
        If delta ==  0.5 - returns ATM call
        If delta == -0.5 - returns ATM put

        If delta > 0.5 - returns ITM call near target delta
        If delta < -0.5 - returns ITM put near target delta

        If delta > 0 and < 0.5 - returns OTM call
        If delta < 0 and > -0.5 - returns OTM put

        If delta <= -1 or >= 1 or 0 - raises error

        Examples:
        # ATM put (delta = -0.5)
        Transaction(opt_chain.get_by_delta(-0.5), date, 1.0),
        # OTM put (delta = -0.25)
        Transaction(opt_chain.get_by_delta(-0.25), date, 1.0),
        # ITM put (delta = -0.75)
        Transaction(opt_chain.get_by_delta(-0.75), date, 1.0),

        # ATM call (delta = 0.5)
        Transaction(opt_chain.get_by_delta(0.5), date, 1.0),
        # OTM call (delta = 0.25)
        Transaction(opt_chain.get_by_delta(0.25), date, 1.0),
        # ITM call (delta = 0.75)
        Transaction(opt_chain.get_by_delta(0.75), date, 1.0),
        """

        # Edit transactions to trade
        trans_list = [
                # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
                #
                #
                ]
        return trans_list

    @staticmethod
    def new_position_bearish_zone(date, fut, opt_chain):
        trans_list = [
                # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
                #
                #
                ]

        return trans_list

    @staticmethod
    def new_position_neutral_zone(date, fut, opt_chain):
        # Edit transactions to trade
        trans_list = [
                # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
                #
                #
            Transaction(opt_chain.get_by_delta(0.05), date, 3.0),
            Transaction(opt_chain.get_by_delta(0.15), date, -3.0),
            Transaction(opt_chain.get_by_delta(-0.05), date, 2.0),
            Transaction(opt_chain.get_by_delta(-0.15), date, -2.0),
        ]
        return trans_list

    def manage_opened_position(self, date, fut, opt_chain, regime, opened_position):
        logging.debug('Current position delta: {0}'.format(opened_position.delta))

        delta = opened_position.delta
        # logging.debug("Last transaction date: {0}".format(opened_position.last_trans_date))
        days_after_last_trans = 0

        if opened_position.last_trans_date is not None:
            days_after_last_trans = relativedelta(date, opened_position.last_trans_date).bdays

        trans_list = []

        if regime == 1:
            # Delta bounds checks for BULLISH regime
            # Check required delta bounds values for position
            if days_after_last_trans > 5 and delta < 0.05 or delta > 0.55:
                # Do not change next
                logging.debug('Rebalancing bullish position')
                trans_list += opened_position.close_all_translist()
                trans_list += self.new_position_bullish_zone(date, fut, opt_chain)
                return trans_list
        if regime == -1:
            # Delta bounds checks for BEARISH regime
            # Check required delta bounds values for position
            if days_after_last_trans > 5 and delta < -0.55 or delta > -0.05:
                # Do not change next
                logging.debug('Rebalancing bearish position')
                trans_list += opened_position.close_all_translist()
                trans_list += self.new_position_bearish_zone(date, fut, opt_chain)
                return trans_list
        if regime == 0:
            # Delta bounds checks for NEUTRAL regime
            # Check required delta bounds values for position
            if days_after_last_trans > 5 and delta < -0.25 or delta > 0.25:
                # Do not change next
                logging.debug('Rebalancing neutral position')
                trans_list += opened_position.close_all_translist()
                trans_list += self.new_position_neutral_zone(date, fut, opt_chain)
                return trans_list
