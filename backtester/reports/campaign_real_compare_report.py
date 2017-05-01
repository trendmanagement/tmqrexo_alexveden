from pymongo import MongoClient
from datetime import datetime
import pprint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class CampaignRealCompare:
    def __init__(self):
        tmp_mongo_connstr = 'mongodb://tmqr:tmqr@10.0.1.2/client-gmi?authMechanism=SCRAM-SHA-1'
        tmp_mongo_db = 'client-gmi'

        mongoClient = MongoClient(tmp_mongo_connstr)
        db = mongoClient[tmp_mongo_db]
        self.collection = db.accountsummarycollection

    def run_compare_report(self, campaign_stats, num_days_back):
        model_tail = pd.DataFrame(campaign_stats['SettleChange'].tail(num_days_back))

        model_tail['Model_Equity'] = pd.DataFrame(
            campaign_stats['SettleChange'].tail(num_days_back)).ffill().cumsum(axis=0)

        model_tail['Model_Costs'] = pd.DataFrame(campaign_stats['Costs'].tail(num_days_back))

        start_date = model_tail.index[0].strftime('%Y-%m-%d')
        Office = 'CLX'
        Account = '60125'

        col_s = self.collection.find(
            {'Batchid': {'$gte': start_date},
             'Office': Office, 'Account': Account, 'SummaryDetailFlag': 'S', 'AccountType': '9Z'})

        col_d = self.collection.find(
            {'Batchid': {'$gte': start_date},
             'Office': Office, 'Account': Account, 'SummaryDetailFlag': 'D'})
        # 'TransactionsCommissionsFees':{'$lt': 0}})

        prev_date = datetime.now()
        table_series_cost = []
        table_series_cost_temp = {}
        # print(table_series_cost_temp)
        for post_d in col_d:
            # pprint.pprint(post)
            date = datetime.strptime(post_d['Batchid'], '%Y-%m-%d')

            if date in table_series_cost_temp:
                # table_series_cost_temp[date] += {'TransactionsCommissionsFees':post_d['TransactionsCommissionsFees']}
                table_series_cost_temp[date]['TransactionsCommissionsFees'] += post_d['TransactionsCommissionsFees']
                table_series_cost_temp[date]['TradedQuantityBuy'] += post_d['TradedQuantityBuy']
                table_series_cost_temp[date]['TradedQuantitySell'] += post_d['TradedQuantitySell']
                # table_series_cost_temp[date][0] += {'TransactionsCommissionsFees':post_d['TransactionsCommissionsFees']}

            else:
                table_series_cost_temp[date] = \
                    {'TransactionsCommissionsFees': post_d['TransactionsCommissionsFees'], \
                     'TradedQuantityBuy': post_d['TradedQuantityBuy'], \
                     'TradedQuantitySell': post_d['TradedQuantitySell']}

        # print(table_series_cost_temp)

        for key, value in table_series_cost_temp.items():
            # print(value)
            table_series_cost_point = {
                'date': key,
                'Real_Costs': value['TransactionsCommissionsFees'],
                'TradedQuantityBuy': value['TradedQuantityBuy'],
                'TradedQuantitySell': value['TradedQuantitySell']
            }

            table_series_cost.append(table_series_cost_point)

        tail_table_cost_real = pd.DataFrame(table_series_cost)
        tail_table_cost_real.index = tail_table_cost_real['date']
        del tail_table_cost_real['date']

        series = []
        table_series = []
        cumValue = 0
        for post_s in col_s:
            # pprint.pprint(post)

            date = datetime.strptime(post_s['Batchid'], '%Y-%m-%d')

            change = post_s['ConvertedChangeInAccountValueAtMarket']
            cumValue += change

            series_point = {
                'date': date,
                'Real_Equity': cumValue
            }

            series.append(series_point)

            table_series_point = {
                'date': date,
                # 'Costs':post_s['TransactionsCommissionsFees'],
                'Real_Equity_Chg': change,
                'Real_Equity': cumValue
            }

            table_series.append(table_series_point)

        tail_plot_real = pd.DataFrame(series)
        tail_plot_real.index = tail_plot_real['date']
        del tail_plot_real['date']
        tail_plot_real['Model_Equity'] = model_tail['Model_Equity']

        tail_table_real = pd.DataFrame(table_series)
        tail_table_real.index = tail_table_real['date']
        del tail_table_real['date']
        tail_table_real['Model_Equity'] = model_tail['Model_Equity']
        tail_table_real['Model_Change'] = model_tail['SettleChange']
        tail_table_real['Real_Buys'] = tail_table_cost_real['TradedQuantityBuy']
        tail_table_real['Real_Sells'] = tail_table_cost_real['TradedQuantitySell']
        tail_table_real['Real_Costs'] = tail_table_cost_real['Real_Costs']
        tail_table_real['Model_Costs'] = model_tail['Model_Costs']

        sum_row = tail_table_real.sum(axis=0)

        # print( tail_table_real)
        # tail_table_real=tail_table_real.append(sum_row)
        print(tail_table_real)
        print('Total_Real_Buys', sum_row['Real_Buys'])
        print('Total_Real_Sells', sum_row['Real_Sells'])
        print('Total_Real_Costs', sum_row['Real_Costs'])
        print('Total_Model_Costs', sum_row['Model_Costs'])

        tail_plot_real.plot()  # ax=ax1,label='At expiration', lw=2, c='blue');
        plt.show()