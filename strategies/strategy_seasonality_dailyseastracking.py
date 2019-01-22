import os

import numpy as np
import pandas as pd
import quandl
from sklearn import preprocessing, ensemble
from backtester.strategy import StrategyBase


class Strategy_Seasonality_DailySeasTracking(StrategyBase):
    name = 'Strategy_Seasonality_DailySeasTracking'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)




    def load_quandl_data(self, quandl_data_link):
        '''
        quandl_data_link must have format like this - 'CHRIS/CME_CL1'
        '''
        if not os.path.exists('/var/data/quandl_data/'):
            os.mkdir('/var/data/quandl_data/')
        quandl_data = quandl.get(quandl_data_link)
        quandl_data_name = quandl_data_link.split('/')[1]
        quandl_data.to_csv('/var/data/quandl_data/' + quandl_data_name)

    def calc_entryexit_rules(self, quandl_data_link, start_year, centered_ma_period, signals_shift, outliers_reduction,
                             rules_index):
        quandl_data_name = quandl_data_link.split('/')[1]

        # https://www.quandl.com/data/CHRIS-Wiki-Continuous-Futures
        '''
        'CHRIS/CME_W1' wheat
        'CHRIS/CME_NG1' nat gas
        'CHRIS/CME_ES1' es
        'CHRIS/CME_C1' corn
        'CHRIS/CME_S1' soy bean
        'CHRIS/CME_CL1' crude oil
        '''
        if not os.path.exists('/var/data/quandl_data/' + quandl_data_name):
            self.load_quandl_data(quandl_data_link)

        quandl_data = pd.read_csv('/var/data/quandl_data/' + quandl_data_name, index_col=0, parse_dates=True)

        if start_year == 'first+1':
            data = quandl_data[(quandl_data.index.year >= (np.unique(quandl_data.index.year)[0] + 1)) &
                               (quandl_data.index.year <= 2009)].resample('B').last().dropna(axis=0, how='all')

        elif start_year != 'first+1':
            data = quandl_data[(quandl_data.index.year >= start_year) &
                               (quandl_data.index.year <= 2009)].resample('B').last().dropna(axis=0, how='all')

        px_ser = self.data.exo

        outliers_reduction = outliers_reduction

        days_a = np.tile(np.arange(1, 32), 12)
        months_a = np.arange(1, 13).repeat(31)

        seasonal_df = pd.DataFrame(index=pd.MultiIndex.from_arrays([days_a, months_a]))

        data_slice = data[(data.index.month >= 1) & (data.index.month <= 12)]
        # data_slice = data[(data.index.month >= 6) & (data.index.month <= 9)]
        # data_slice = data[(data.index.day >= 1) & (data.index.day <= 10)]
        # data_slice = data[(data.index.day >= 1) & (data.index.day <= 15)]

        # Outliers detection model
        if outliers_reduction == True:
            od_model = ensemble.IsolationForest(n_estimators=100, contamination=0.3, random_state=0)
            # od_model = covariance.EllipticEnvelope(contamination=0.2, assume_centered=True)
            # od_model = svm.OneClassSVM()
            reduction_coef = 3

        for y in np.unique(data_slice.index.year):
            if outliers_reduction == True:
                # data_slice_yearly = data_slice[data_slice.index.year == y].Last.diff().dropna()
                data_slice_yearly = data_slice[data_slice.index.year == y].Last.rolling(centered_ma_period,
                                                                                        center=True).mean().diff().dropna()

            elif outliers_reduction == False:
                # data_slice_yearly = data_slice[data_slice.index.year == y].Last.dropna()
                data_slice_yearly = data_slice[data_slice.index.year == y].Last.rolling(centered_ma_period,
                                                                                        center=True).mean().dropna()

            data_slice_yearly.values[:] = preprocessing.StandardScaler().fit_transform(
                data_slice_yearly.values.reshape(-1, 1)).ravel()

            if outliers_reduction == True:
                od_model.fit(data_slice_yearly.reshape(-1, 1))
                data_slice_yearly.loc[
                    od_model.predict(data_slice_yearly.reshape(-1, 1)) == -1] = data_slice_yearly / reduction_coef
                data_slice_yearly = data_slice_yearly.cumsum()

            seasonal_df[str(y)] = pd.Series(data_slice_yearly.values,
                                            index=[data_slice_yearly.index.day, data_slice_yearly.index.month])

        seasonal_df.index.set_names(('day', 'month'), inplace=True)
        seasonal_df = seasonal_df.dropna(how='all').reset_index().interpolate(method='linear').set_index(
            ['day', 'month'])

        if outliers_reduction == True:
            seasonal_df.dropna(inplace=True)
            seasonal_df.values[:] = preprocessing.StandardScaler().fit_transform(seasonal_df.values[:])

        seasonal_avg_px = seasonal_df.mean(axis=1)
        seasonal_avg_px.name = 'seas_avg'
        seasonal_avg_px = seasonal_avg_px.copy().reset_index()
        seasonal_avg_px['long_signal'] = seasonal_avg_px['seas_avg'].diff().shift(-signals_shift) > 0
        seasonal_avg_px['short_signal'] = seasonal_avg_px['seas_avg'].diff().shift(-signals_shift) < 0

        if rules_index == 0:
            trigger_ser = pd.Series(False, index=px_ser.index)
            for idx in trigger_ser.index:
                trigger = seasonal_avg_px[(seasonal_avg_px.month == idx.month) &
                                          (seasonal_avg_px.day == idx.day)].long_signal.values

                if trigger.size != 0:
                    trigger_ser.ix[idx] = trigger[0]

            entry_rule = trigger_ser == True
            exit_rule = trigger_ser == False

            return entry_rule, exit_rule

        if rules_index == 1:
            trigger_ser = pd.Series(False, index=px_ser.index)
            for idx in trigger_ser.index:
                trigger = seasonal_avg_px[(seasonal_avg_px.month == idx.month) &
                                          (seasonal_avg_px.day == idx.day)].short_signal.values

                if trigger.size != 0:
                    trigger_ser.ix[idx] = trigger[0]

            entry_rule = trigger_ser == True
            exit_rule = trigger_ser == False

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
            direction, quandl_data_link, start_year, centered_ma_period, signals_shift, outliers_reduction, rules_index = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, quandl_data_link, start_year, centered_ma_period, signals_shift, outliers_reduction, rules_index = params

        # Enry/exit rules
        entry_rule, exit_rule = self.calc_entryexit_rules(quandl_data_link, start_year,
                                                          centered_ma_period, signals_shift, outliers_reduction,
                                                          rules_index)

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None

        return swarm_member_name, entry_rule, exit_rule, calc_info