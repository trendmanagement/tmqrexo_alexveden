from sklearn import (pipeline, preprocessing, ensemble, neighbors, linear_model, neural_network, cluster, metrics,
                     decomposition,
                     naive_bayes, calibration, svm, multioutput,
                     feature_selection, discriminant_analysis, model_selection, multiclass
                     )

from scipy import signal, ndimage
import numpy as np
import pandas as pd
from backtester.strategy import StrategyBase



class Strategy_DSP_BandPassML(StrategyBase):
    name = 'Strategy_DSP_BandPass'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    def calc_entryexit_rules(self, filt_order, filt_start_f, filt_stop_f, pred_horizon, rule_index):
        px_ser = self.data.exo

        b, a = signal.butter(filt_order, [filt_start_f, filt_stop_f], btype='bandpass')

        filtered_ser = px_ser.copy()
        filtered_ser.values[:] = signal.lfilter(b, a, filtered_ser)

        # filtered_ser.to_csv('temp_data/bp_filter_ser.csv')

        # filtered_ser = universal_fisher_transform_expwindow(filtered_ser, transform_with='arctanh')
        filtered_ser = pd.Series.from_csv('temp_data/bp_filter_ser.csv')
        # filtered_ser = filtered_ser.ix[px_ser.index]

        dataset_df = pd.DataFrame(index=filtered_ser.index)

        for p in range(1, 100, 1):
            dataset_df['features_prev_val{0}'.format(p)] = filtered_ser.shift(p)
            dataset_df['features_updn_moves_rollingsum{0}'.format(p)] = (filtered_ser.diff() > 0).astype(
                np.float32).replace(0, -1).rolling(p).sum()

        for order, wn in zip(range(1, 4), np.arange(0.0, 0.9, 0.01)):
            b, a = signal.butter(order, wn, btype='lowpass')
            dataset_df['features_lpfilter{0}_{1}'.format(order, wn)] = signal.lfilter(b, a, filtered_ser.values[:])

        dataset_df['target'] = filtered_ser.shift(-pred_horizon)

        dataset_df.ffill(inplace=True)
        dataset_df.dropna(inplace=True)

        train_features = dataset_df.filter(regex='features').ix[:'2013']
        train_target = dataset_df.target.ix[:'2013']

        test_features = dataset_df.filter(regex='features').ix[:]
        test_target = dataset_df.target.ix[:]

        # test_features = dataset_df.filter(regex='features').ix[train_features.index[-1]:]
        # test_target = dataset_df.target.ix[train_features.index[-1]:]

        scaler = preprocessing.RobustScaler()

        model = pipeline.Pipeline([('scaler', scaler),
                                   ('regmodel',
                                    ensemble.BaggingRegressor(linear_model.HuberRegressor(), n_estimators=100,
                                                              random_state=0))
                                   ])

        model.fit(train_features, train_target)

        df = pd.DataFrame(index=px_ser.index)
        df['filter'] = filtered_ser
        df['prediction'] = pd.Series(model.predict(test_features), index=test_features.index)
        df['target'] = test_target

        if rule_index == 0:
            entry_rule = (df['filter'] > df['prediction'])
            exit_rule = (df['filter'] < df['prediction'])

            return entry_rule, exit_rule

        elif rule_index == 1:
            entry_rule = df['filter'] < df['prediction']
            exit_rule = df['filter'] > df['prediction']

            return entry_rule, exit_rule

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
            (direction, filt_order, filt_start_f, filt_stop_f, pred_horizon, rules_index) = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            (direction, filt_order, filt_start_f, filt_stop_f, pred_horizon, rules_index) = params

        # Defining EXO price
        px = self.data.exo

        entry_rule, exit_rule = self.calc_entryexit_rules(filt_order, filt_start_f, filt_stop_f, pred_horizon,
                                                          rules_index)

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None
        return swarm_member_name, entry_rule, exit_rule, calc_info