import pandas as pd
import time
from tqdm import tqdm, tnrange, tqdm_notebook
import numpy as np
import sys


def ipython_info():
    ip = False
    if 'ipykernel' in sys.modules:
        ip = 'notebook'
    elif 'IPython' in sys.modules:
        ip = 'terminal'
    return ip

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

    @staticmethod
    def comp_results_dataframe(full, temp):
        """
        Compare results of 2 dataframes
        :param full:
        :param temp:
        :return:
        """
        if isinstance(temp, pd.DataFrame):
            has_errs = False

            for col in temp.columns:
                if col not in full:
                    raise ValueError("Column '{0}' doesn't exist in full historical results dataframe".format(col))
                s_full = full[col].dropna()
                s_temp = temp[col].dropna()

                if not np.alltrue(s_temp == s_full.ix[s_temp.index]):
                    print("Column:{0} Results don't match exactly. Future ref suspected.".format(col))
                    diff = s_temp - s_full.ix[s_temp.index]
                    print('Difference: ')
                    print(diff[diff != 0.0].dropna())
                    has_errs = True

            return not has_errs
        else:
            raise ValueError("Result of 'algo_func' should be pandas.DataFrame got {0}".format(type(temp)))

    @staticmethod
    def comp_results_series(full, temp):
        """
        Compare results of 2 Series
        :param full:
        :param temp:
        :return:
        """
        if isinstance(temp, pd.Series):
            if not np.alltrue(temp == full.ix[temp.index]):
                print("Results don't match exactly. Future ref suspected.")
                diff = temp - full.ix[temp.index]
                print('Difference: ')
                print(diff[diff != 0.0].dropna())
                return False
            else:
                return True
        else:
            raise ValueError("Result of 'algo_func' should be pandas.Series got {0}".format(type(temp)))

    @staticmethod
    def test_algo(data, compare_func, algo_func, *args, **kwargs):
        """
        Test future reference problems with algo_func
        :param data: pd.DataFrame or Series of initial data
        :param compare_func: Comparison function to check data equality
        :param algo_func: algorithm to test
        :param args:  args passed to algorithm
        :param kwargs: kwargs passed to algorithm
        :return:
        """
        if not isinstance(data, pd.DataFrame) and not isinstance(data, pd.Series):
            raise ValueError("'data' should be pandas.DataFrame or pandas.Series")

        print('Starting algo sanity checks')
        day_step = 5
        nsteps = int((len(data) * 0.8) / day_step)
        istart = int(len(data) * 0.2)

        algo_result_full = algo_func(data, *args, **kwargs)

        #print("Steps to go {0}".format(nsteps))

        if ipython_info() == 'notebook':
            pbar = tqdm_notebook(desc="Progress", total=nsteps)
        else:
            pbar = tqdm(desc="Progress", total=nsteps)

        for i in range(nsteps):
            data_chunk = data.iloc[:istart + day_step*i]
            t_algo_result = algo_func(data_chunk, *args, **kwargs)
            if not compare_func(algo_result_full, t_algo_result):
                print("Algorithm fut-ref sanity check failed, on step # {0} Date: {1}".format(i, data_chunk.index[-1]))
                break
            pbar.update(1)

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

