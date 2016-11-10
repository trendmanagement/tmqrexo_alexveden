# coding: utf-8

# In[2]:

import sys, os

from backtester.strategy import StrategyBase, OptParam
import pandas as pd


class StrategyEXO(StrategyBase):
    name = 'EXO'


    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    def calculate(self, params=None, save_info=False):

        if params is None:
            # Return default parameters
            direction = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction = params

        # Defining EXO price
        px = self.data.exo

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None
        if save_info:
            calc_info = {}

        return swarm_member_name, pd.Series(True, index=px.index), pd.Series(False, index=px.index), calc_info

