import itertools
import numpy as np


class OptParam(object):
    """
    Generic system optimization parameter, like Moving Avg period etc..
    """
    def __init__(self, name, default_value, min_value, max_value, step):
        self.name = name
        self.default = default_value
        self.min = min_value
        self.max = max_value
        self.step = step


class StrategyBase(object):
    """
    Base class for swarming strategy
    """
    def __init__(self):
        self.name = 'BaseStrategy'
        self.opts = None

    def slice_opts(self):
        if self.opts is None:
            return [None]
        result = []
        for o in self.opts:
            result.append(np.arange(o.min, o.max, o.step))
        return itertools.product(*result)

    def default_opts(self):
        """
        Returns default tuple params for opts
        :return:
        """
        if self.opts is None:
            return None
        results = []

        for o in self.opts:
            results.append(o.default)
        return tuple(results)



    def run_swarm(self, save_equity=False):
        '''
        Brute force all steps of self.opts and calculate base stats
        '''
        result = []
        # loop through all steps of every OptParam
        # Calculate algo
        # Store the results
        for opts in self.slice_opts():
           equity, stats = self.calculate(opts)
           result.append(
            [
                opts,
                stats,
                equity if save_equity else None
            ]
           )

        return result


    def calculate(self,params=None):
        """
        The main method for trading logics calculation
        :param params: tuple-like object with optimizations parameters
        :return:
        """
        return None, None