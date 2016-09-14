# coding: utf-8

# In[2]:

import sys, os

sys.path.append('..')
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam

import pandas as pd
import numpy as np
import scipy

from sklearn import tree, neighbors, ensemble
from sklearn import metrics, grid_search, cross_validation, preprocessing

class StrategyMachineLearnedSimple(StrategyBase):
    name = 'MachineLearnedSimple'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    def calculate(self, params=None, save_info=False):
        #
        #
        #  Params is a tripple like (50, 10, 15), where:
        #   50 - slow MA period
        #   10 - fast MA period
        #   15 - median period
        #
        #  On every iteration of swarming algorithm, parameter set will be different.
        #  For more information look inside: /notebooks/tmp/Swarming engine research.ipynb
        #

        if params is None:
            # Return default parameters
            direction, prediction_window, price_smoothing_period, period_median = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, prediction_window, price_smoothing_period, period_median = params

        # Defining EXO price
        px = self.data.exo

        df = pd.DataFrame()
        # df['close'] = d.exo.ix[:'2014']
        df['close'] = self.data.exo.ix[:]

        df.close = df.close.rolling(price_smoothing_period).mean()

        for i in range(10, 100, 10):
            df['rel_str_' + str(i)] = df.close - df.close.rolling(i).mean()

            df['price_above_ma' + str(i)] = df.close > df.close.rolling(i).mean()
            df['price_below_ma' + str(i)] = df.close < df.close.rolling(i).mean()

            df['price_change_skew_' + str(i)] = df.close.diff().rolling(i).skew()

        df = df.dropna()

        df = pd.DataFrame(preprocessing.scale(df), index=df.index, columns=df.columns)

        if direction == -1:
            df['target'] = (df.close.shift(-prediction_window) - df.close) < 0

        elif direction == 1:
            df['target'] = (df.close.shift(-prediction_window) - df.close) > 0


        train_features = df.drop('target', 1).ix[:'2013']
        train_target = df.target.ix[:'2013']

        test_features = df.drop('target', 1).ix[:]
        test_target = df.target.ix[:]

        model = neighbors.KNeighborsClassifier(n_neighbors=5)
        #model = model = ensemble.RandomForestClassifier(n_estimators=100)

        param_range = list(range(2, 100, 1))
        param_grid = dict(n_neighbors=param_range)

        #param_range = list(range(1,200,1))
        #param_grid = dict(n_estimators=param_range)

        # param_range = np.arange(0.01,2,0.01)
        # param_grid = dict(C=param_range)

        grid = grid_search.RandomizedSearchCV(model, param_grid, cv=10, scoring='average_precision', n_jobs=-1)
        grid.fit(train_features, train_target)

        df['prediction'] = grid.predict(test_features)

        # df = pd.concat([df,self.data], join='inner', axis=1)
        #signal_df = self.data.join(df.prediction, how='outer').fillna(False)

        # Median based trailing stop
        trailing_stop = px.rolling(period_median).median().shift(1)

        # Enry/exit rules
        entry_rule = self.data.join(df.prediction, how='outer').fillna(False).prediction == True

        if direction == 1:
            exit_rule = (CrossDown(px, trailing_stop))  # Cross down for longs

        elif direction == -1:
            exit_rule = (CrossUp(px, trailing_stop))  # Cross up for shorts, Cross down for longs

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None
        if save_info:
            calc_info = {'trailing_stop': trailing_stop}

        return swarm_member_name, entry_rule, exit_rule, calc_info


if __name__ == "__main__":
    #
    #   Run this code only from direct shell execution
    #
    # strategy = StrategyMACrossTrail()
    # equity, stats = strategy.calculate()

    # Do some work
    data, info = matlab.loaddata('../mat/strategy_270225.mat')
    data.plot()


# In[ ]:
