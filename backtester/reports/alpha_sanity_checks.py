import pandas as pd
import time
from tqdm import tqdm, tnrange, tqdm_notebook
import numpy as np

class AlphaSanityChecker:
    def __init__(self, swarm, day_step=5, initial_window=500):
        self.swarm = swarm
        self.day_step = int(day_step)
        self.initial_window = initial_window
        self.strategy = self.swarm.strategy

        if self.day_step <= 0:
            raise ValueError('day_step must be positive integer')

        if self.initial_window <= 0:
            raise ValueError("initial_window must be positive")

        if self.initial_window > len(self.strategy.data):
            raise ValueError("Not enough EXO data or initial_window is too long.")



    def process_opts(self, opt, full_data):
        nsteps = int((len(full_data)-self.initial_window) / self.day_step)

        #
        # Process strategy algorithm based on full data
        #
        self.strategy.data = full_data

        #return swarm_member_name, entry_rule, exit_rule, calc_info
        swarm_member_name, entry_rule, exit_rule, calc_info = self.strategy.calculate(opt)

        for i in range(nsteps): #tqdm_notebook(range(nsteps), desc='Opt: ' + swarm_member_name, leave=False):
            self.strategy.data = full_data.iloc[:self.initial_window + self.day_step*i]

            t_swarm_member_name, t_entry_rule, t_exit_rule, calc_info = self.strategy.calculate(opt)

            if not np.alltrue((entry_rule.ix[t_entry_rule.index] == t_entry_rule)):
                print("{0} Entry rules don't match exactly. Future ref suspected.".format(swarm_member_name))
                return False

            if not np.alltrue((exit_rule.ix[t_exit_rule.index] == t_exit_rule)):
                print("{0} Exit rules don't match exactly. Future ref suspected.".format(swarm_member_name))
                return False

        self.strategy.data = full_data

        return True

    def run(self):
        data = self.strategy.data


        opt_list = self.strategy.slice_opts()
        max_steps = len(self.swarm.raw_swarm.columns)

        has_errors = False

        for opt in tqdm_notebook(opt_list, desc="Progress", total=max_steps):
            if not self.process_opts(opt, data):
                has_errors = True

        self.strategy.data = data
        if has_errors:
            print("Alpha algorithm seems to have future reference issues")
        else:
            print("Alpha algorithm seems to be VALID")

        print('Finished')

