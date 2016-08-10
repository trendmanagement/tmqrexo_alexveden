
# coding: utf-8

# In[1]:

import sys,os
sys.path.append('..')
sys.path.append('../..')
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.swarms.manager import SwarmManager
from backtester.exoinfo import EXOInfo

import pandas as pd
import numpy as np
import scipy

import glob
from pandas.tseries.offsets import *

for file in glob.glob("./temp_swarms/*.swm"):

    # set file name here

    # Real swarm from .swm
    df = SwarmManager.load(file)
    df = df.swarm

    print('calculating portfolio for ---', file)
    # ## Systems overall performance estimation

    # In[6]:

    temp_l = []

    for strat in df.columns:

            input_strategy_data = df[strat] # This data is used in metrics calc

            price_change = input_strategy_data.diff()
            max_dd = (input_strategy_data - input_strategy_data.expanding().max()).min()
            netprofit = df[strat].ix[-1] - df[strat].ix[0]

            # Since swarm PnL statistics is not trade-by-trade
            # For PF calc I used cumulative values of positive and negatives price changes
            # Same for winrate
            profit_factor = price_change[price_change > 0].sum() / np.abs(price_change[price_change < 0].sum())

            winrate = (price_change[price_change > 0].count() / price_change.count()) * 100

            try:
                modsharpe = np.mean(price_change) / np.std(price_change)

            except ZeroDivisionError:
                modsharpe = np.nan

            d = {'strategy': strat,
                'stats_pricechange_modsharpe': modsharpe,
                'stats_netprofit': netprofit,
                'stats_max_dd': max_dd, 'stats_recovery_factor': netprofit / np.abs(max_dd),
                'stats_profit_factor': profit_factor, 'stats_winrate': winrate }

            temp_l.append(d)


    # In[7]:

    strategies_performance_df = pd.DataFrame(temp_l).dropna()
    strategies_performance_df['rank_score'] = np.zeros_like(len(strategies_performance_df))
    strategies_performance_df


    # ## Strategies overall performance ranking

    # In[8]:

    ranks_d = {}

    for col in strategies_performance_df.columns:

        stats_col_flag = False

        if 'stats' in col:

            # Define 0-10-20-30-40-50-60-70-80-90-100 quantiles values of certain strategy statistics
            metric_quantile0 = strategies_performance_df[col].quantile(0.0)
            metric_quantile10 = strategies_performance_df[col].quantile(0.1)
            metric_quantile20 = strategies_performance_df[col].quantile(0.2)
            metric_quantile30 = strategies_performance_df[col].quantile(0.3)
            metric_quantile40 = strategies_performance_df[col].quantile(0.4)
            metric_quantile50 = strategies_performance_df[col].quantile(0.5)
            metric_quantile60 = strategies_performance_df[col].quantile(0.6)
            metric_quantile70 = strategies_performance_df[col].quantile(0.7)
            metric_quantile80 = strategies_performance_df[col].quantile(0.8)
            metric_quantile90 = strategies_performance_df[col].quantile(0.9)
            metric_quantile100 = strategies_performance_df[col].quantile(1)

            stats_col_flag = True

        if stats_col_flag == True:

            for strat in strategies_performance_df.strategy:

                # Define strategy statistics rank of certain strategy

                strategy_stats_metric = strategies_performance_df[strategies_performance_df.strategy == strat][col].values[0]

                if strategy_stats_metric >= metric_quantile0 and strategy_stats_metric <= metric_quantile10:
                    rank_score = 0

                elif strategy_stats_metric >= metric_quantile10 and strategy_stats_metric <= metric_quantile20:
                    rank_score = 1

                elif strategy_stats_metric >= metric_quantile20 and strategy_stats_metric <= metric_quantile30:
                    rank_score = 2

                elif strategy_stats_metric >= metric_quantile30 and strategy_stats_metric <= metric_quantile40:
                    rank_score = 3

                elif strategy_stats_metric >= metric_quantile40 and strategy_stats_metric <= metric_quantile50:
                    rank_score = 4

                elif strategy_stats_metric >= metric_quantile50 and strategy_stats_metric <= metric_quantile60:
                    rank_score = 5

                elif strategy_stats_metric >= metric_quantile60 and strategy_stats_metric <= metric_quantile70:
                    rank_score = 6

                elif strategy_stats_metric >= metric_quantile70 and strategy_stats_metric <= metric_quantile80:
                    rank_score = 7

                elif strategy_stats_metric >= metric_quantile80 and strategy_stats_metric <= metric_quantile90:
                    rank_score = 8

                elif strategy_stats_metric >= metric_quantile90 and strategy_stats_metric <= metric_quantile100:
                    rank_score = 9

                elif strategy_stats_metric == metric_quantile100:
                    rank_score = 10


                if strat not in ranks_d.keys():
                    ranks_d[strat] = rank_score

                elif strat in ranks_d.keys():
                    ranks_d[strat] = ranks_d[strat] + rank_score

                # For debugging purposes

                #print('strategy---',strat,'\n')
                #print(col)
                #print('10 quantile---',metric_quantile10)
                #print(strategy_stats_metric)
                #print('60 quantile---',metric_quantile60)
                #print(strategy_stats_metric > metric_quantile40 and strategy_stats_metric < metric_quantile50)
                #print('rank_score------', rank_score, '\n')

            #print("NEXT----------------------- \n")

    # Set rank scores for strategies from dict

    for k in ranks_d:

        strat_index = strategies_performance_df[strategies_performance_df.strategy == k].index
        strategies_performance_df = strategies_performance_df.set_value(strat_index, 'rank_score', ranks_d[k])


    # In[9]:

    strategies_performance_df.sort_values('rank_score', ascending=False)


    # ## Drop all strategies which have rank score less than n quantile value

    # In[10]:

    df = df[strategies_performance_df[strategies_performance_df.rank_score >= strategies_performance_df.rank_score.quantile(0.5)].strategy]


    # In[11]:



    # ## Filter those strategies by correlation

    # In[12]:

    # Rearrange columns from best to worst strategies
    df = df.reindex_axis(strategies_performance_df.sort_values('rank_score', ascending=False).strategy, axis=1).dropna(axis=1).asfreq(BDay())



    corr_df = df.corr()

    while_loop_break_flag = False

    while True:
        if while_loop_break_flag == False:

            for i in range(len(corr_df)):

                try:
                    strat_corr = corr_df[corr_df.columns[i]]

                except IndexError:
                    strat_corr = corr_df[corr_df.columns[-1]]

                df = df.drop(strat_corr[(strat_corr.index != strat_corr.name) & (strat_corr >= 0.5)].index, axis=1)

                # Check if previous DF are the same as current DF
                # If they are different - continue the loop

                df_comparison_array = np.array_equal(corr_df,df.corr())

                #print(strat_corr[(strat_corr.index != strat_corr.name) & (strat_corr >= 0.5)].index)
                #print(i)
                #print(len(corr_df))
                #print(len(corr_df))

                if df_comparison_array  == False and i < len(corr_df):
                    corr_df = df.corr()

                elif df_comparison_array  == True and i == len(corr_df)-1:
                    while_loop_break_flag = True
                    break

        if while_loop_break_flag == True:
            break





    # # Metrics calculation

    # In[17]:

    #
    # Rebalance triggers
    #
    # Rebalance trigger must be array of Datetime indexes when event occurred, like date of monday or new month
    #
    newmonth = df[df.index.month != df.index.shift(1).month].index

    monday = df[df.index.weekday == 0].index

    norebalance = [df.index[-1]]

    newyear = df[df.index.year != df.index.shift(1).year].index
    #
    #
    #

    # note: I think more performance metrics for strategies is better
    # https://www.amibroker.com/guide/h_report.html for reference

    rebalance_index = 1
    rebalance_date_start = None

    rebalance_trigger = monday # set rebalance trigger here

    temp_l = []

    for reb_idx in rebalance_trigger:

        for strat in df.columns:

            if rebalance_index == 1:
                rebalance_date_start = df.index[0]

            for i in range(len(df[strat])):

                if df[strat].index[i] == reb_idx:

                    input_strategy_data = df[strat].ix[rebalance_date_start:reb_idx] # This data is used in metrics calc

                    price_change = input_strategy_data.diff()
                    max_dd = (input_strategy_data - input_strategy_data.expanding().max()).min()
                    netprofit = df[strat].ix[reb_idx] - df[strat].ix[rebalance_date_start]

                    # Since swarm PnL statistics is not trade-by-trade
                    # For PF calc I used cumulative values of positive and negatives price changes
                    # Same for winrate
                    profit_factor = price_change[price_change > 0].sum() / np.abs(price_change[price_change < 0].sum())

                    winrate = (price_change[price_change > 0].count() / price_change.count()) * 100
                    # If all trades are negative, PF is 0. But later all 0s is replaced with NaN.
                    # To avoid replacing true 0.0 PF set it to 0.000001
                    # This made for handling missing data

                    # Also winrate can be 0.0, but if PF is NaN - no trades were made
                    # This made for handling missing data

                    if winrate == 0.0 and np.isnan(profit_factor) == False:
                        winrate = 0.000001

                    elif winrate == 0.0 and np.isnan(profit_factor) == True:
                        winrate = np.nan

                    if profit_factor == 0.0:
                        profit_factor = 0.000001

                    try:
                        modsharpe = np.mean(price_change) / np.std(price_change)

                    except ZeroDivisionError:
                        modsharpe = np.nan


                    d = {'strategy': strat,'rebalance_date_start': rebalance_date_start,
                        'rebalance_date_end': reb_idx, 'rebalance_index': rebalance_index,
                        'stats_pricechange_modsharpe': modsharpe,
                        'stats_netprofit': netprofit,
                        'stats_max_dd': max_dd, 'stats_recovery_factor': netprofit / np.abs(max_dd),
                        'stats_profit_factor': profit_factor, 'stats_winrate': winrate }

                    '''
                    d = {'strategy': strat,'rebalance_date_start': rebalance_date_start,
                        'rebalance_date_end': reb_idx, 'rebalance_index': rebalance_index,
                        'stats_pricechange_modsharpe': modsharpe,
                        'stats_recovery_factor': netprofit / np.abs(max_dd)}
                    '''

                    temp_l.append(d)

        rebalance_index += 1
        rebalance_date_start = reb_idx # set new start rebalance date to current rebalance trigger date


    # ### Data cleaning

    # In[18]:

    # Replacing 0 values with NaNs
    # If strategy stats is 0 means that no trades were made
    stats_df = pd.DataFrame(temp_l).replace(0, np.nan)

    # Filling NaNs with last avaible values
    for s in stats_df.strategy.unique():
        stats_df[stats_df.strategy == s] = stats_df[stats_df.strategy == s].fillna(method='pad')

    stats_df = stats_df.dropna(how='any')


    ranks_d = {}
    ranks_rebidx_d = {}

    for i in stats_df.rebalance_index.unique():

        for col in stats_df[stats_df.rebalance_index == i].columns:

            stats_col_flag = False

            if 'stats' in col:

                # Define 0-10-20-30-40-50-60-70-80-90-100 quantiles values of certain strategy statistics
                metric_quantile0 = stats_df[col].quantile(0.0)
                metric_quantile10 = stats_df[col].quantile(0.1)
                metric_quantile20 = stats_df[col].quantile(0.2)
                metric_quantile30 = stats_df[col].quantile(0.3)
                metric_quantile40 = stats_df[col].quantile(0.4)
                metric_quantile50 = stats_df[col].quantile(0.5)
                metric_quantile60 = stats_df[col].quantile(0.6)
                metric_quantile70 = stats_df[col].quantile(0.7)
                metric_quantile80 = stats_df[col].quantile(0.8)
                metric_quantile90 = stats_df[col].quantile(0.9)
                metric_quantile100 = stats_df[col].quantile(1)

                stats_col_flag = True

            if stats_col_flag == True:

                for strat in stats_df[stats_df.rebalance_index == i].strategy:

                    # Define strategy statistics rank of certain strategy

                    strategy_stats_metric = stats_df[(stats_df.rebalance_index == i)
                                                     & (stats_df.strategy == strat)][col].values[0]

                    if strategy_stats_metric >= metric_quantile0 and strategy_stats_metric <= metric_quantile10:
                        rank_score = 0

                    elif strategy_stats_metric >= metric_quantile10 and strategy_stats_metric <= metric_quantile20:
                        rank_score = 1

                    elif strategy_stats_metric >= metric_quantile20 and strategy_stats_metric <= metric_quantile30:
                        rank_score = 2

                    elif strategy_stats_metric >= metric_quantile30 and strategy_stats_metric <= metric_quantile40:
                        rank_score = 3

                    elif strategy_stats_metric >= metric_quantile40 and strategy_stats_metric <= metric_quantile50:
                        rank_score = 4

                    elif strategy_stats_metric >= metric_quantile50 and strategy_stats_metric <= metric_quantile60:
                        rank_score = 5

                    elif strategy_stats_metric >= metric_quantile60 and strategy_stats_metric <= metric_quantile70:
                        rank_score = 6

                    elif strategy_stats_metric >= metric_quantile70 and strategy_stats_metric <= metric_quantile80:
                        rank_score = 7

                    elif strategy_stats_metric >= metric_quantile80 and strategy_stats_metric <= metric_quantile90:
                        rank_score = 8

                    elif strategy_stats_metric >= metric_quantile90 and strategy_stats_metric <= metric_quantile100:
                        rank_score = 9

                    elif strategy_stats_metric == metric_quantile100:
                        rank_score = 10


                    if strat not in ranks_d.keys():
                        ranks_d[strat] = rank_score

                    elif strat in ranks_d.keys():
                        ranks_d[strat] = ranks_d[strat] + rank_score
                #ranks_d['rebalance_idx_'+str(i)] = i


                    # For debugging purposes

                    #print('strategy---',strat,'\n')
                    #print(col)
                    #print('10 quantile---',metric_quantile10)
                    #print(strategy_stats_metric)
                    #print('60 quantile---',metric_quantile60)
                    #print(strategy_stats_metric > metric_quantile40 and strategy_stats_metric < metric_quantile50)
                    #print('rank_score------', rank_score, '\n')


        #print('rebalance index ---', i)
        #break
        for k in ranks_d:

            strat_index = stats_df[(stats_df.strategy == k) & ((stats_df.rebalance_index == i))].index
            #print(strat_index)
            stats_df = stats_df.set_value(strat_index, 'rank_score', ranks_d[k])

        ranks_d = {}


    # ### Strategies picker

    # In[21]:

    # Trade-by-trade pnl
    pnl_df = df.diff()

    summary_best_eqty = pd.Series()
    summary_worst_eqty = pd.Series()
    benchmark_eqty = pd.Series()
    # We can set start rebalance index value to
    for i in range(stats_df.rebalance_index.unique().min(),stats_df.rebalance_index.unique().max()):

        if i < 2:
            # We must estimate strategies preformance at least on one rebalance window
            continue

        else:

            # Pick strats from previous rebalance, but trade them until next rebalance

            start_date = stats_df[stats_df.rebalance_index == i].rebalance_date_start.values[0]
            end_date = stats_df[stats_df.rebalance_index == i].rebalance_date_end.values[0]

            # Number of picked strats defined by .strategy.values[:number]
            # Remove -1 from 'i - 1' to get holy grail :D (future reference)

            picked_best_strats = stats_df[stats_df.rebalance_index == i - 1].sort_values('rank_score',
                                                                                    ascending=False).strategy.values[:2]

            picked_worst_strats = stats_df[stats_df.rebalance_index == i - 1].sort_values('rank_score',
                                                                                    ascending=False).strategy.values[-2:]

            all_strats = stats_df[stats_df.rebalance_index == i - 1].sort_values('rank_score',
                                                                                    ascending=False).strategy.values[:]

            if len(summary_best_eqty) == 0 and len(summary_worst_eqty) == 0 and len(benchmark_eqty) == 0:
                summary_best_eqty = df[picked_best_strats].ix[start_date : end_date].sum(axis=1)
                summary_worst_eqty = pnl_df[picked_worst_strats].ix[start_date : end_date].sum(axis=1)

                benchmark_eqty = pnl_df[all_strats].ix[start_date : end_date].sum(axis=1)

            else:
                summary_best_eqty = summary_best_eqty.append(pnl_df[picked_best_strats].ix[start_date : end_date].sum(axis=1))
                summary_worst_eqty = summary_worst_eqty.append(pnl_df[picked_worst_strats].ix[start_date : end_date].sum(axis=1))

                benchmark_eqty = benchmark_eqty.append(pnl_df[all_strats].ix[start_date : end_date].sum(axis=1))


    best_portfolio = summary_best_eqty.cumsum()
    worst_portfolio = summary_worst_eqty.cumsum() * -1 # Reversed

    summary_portfolio = best_portfolio + worst_portfolio

    benchmark_portfolio = benchmark_eqty.cumsum()

    best_portfolio.to_csv('./portfolios/'+file.split('\\')[1].split('.')[0]+'.csv')
    print(file.split('\\')[1].split('.')[0], "----DONE")
