from collections import OrderedDict

import pandas as pd
from pymongo import MongoClient

from exobuilder.exo.position import Position
from scripts.settings import *


class CampaignRealCompare:
    def __init__(self):
        tmp_mongo_connstr = 'mongodb://tmqr:tmqr@10.0.1.2/client-gmi?authMechanism=SCRAM-SHA-1'
        tmp_mongo_db = 'client-gmi'

        mongoClient = MongoClient(tmp_mongo_connstr)
        db = mongoClient[tmp_mongo_db]
        self.collection = db.accountsummarycollection



    def _calc_transactions(self, date, current_pos, prev_pos):
        result = {}
        assert current_pos is not None, 'current_pos must be initialized'

        if prev_pos is None:
            intersected_assets = set(current_pos)
        else:
            intersected_assets = set(current_pos) | set(prev_pos)

        for asset in intersected_assets:
            prev_values = prev_pos.get(asset, None) if prev_pos is not None else None
            curr_values = current_pos.get(asset, None)

            if prev_values is None:
                result[asset] = curr_values
            elif curr_values is None:
                # Skip old closed positions
                if prev_values != 0:
                    result[asset] = -prev_values
            else:
                # Calculating transactions for existing position
                trans_qty = curr_values - prev_values

                result[asset] = trans_qty
        return result

    def get_account_positions_archive_pnl(self, account_name, instrument, costs_per_option=3.0, costs_per_contract=3.0,
                                          num_days_back=20):

        mongoClient = MongoClient(MONGO_CONNSTR)
        db = mongoClient[MONGO_EXO_DB]

        storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, 4, 20, storage)

        position_dict = OrderedDict()

        for pos in reversed(list(db['accounts_positions_archive'].find({'name': account_name}).sort([('date_now', -1)]).limit(num_days_back))):
            # print(pos)

            dt = pos['date_now']
            pos_rec = position_dict.setdefault(dt, {})

            for p in pos['positions']:
                if '_hash' not in p['asset']:
                    break

                pos_rec[p['asset']['_hash']] = p['qty']

        prev_position = None

        account_pnl = []
        costs = []
        account_pnl_index = []

        p_dict = Position().as_dict()


        for d, pos_rec in position_dict.items():
            costs_sum = 0.0

            asset_info = assetindex.get_instrument_info(instrument)
            exec_time_end, decision_time_end = AssetIndexMongo.get_exec_time(d, asset_info)

            position = Position.from_dict(p_dict, datasource, decision_time_end)

            # print('\n\nDate: {0}'.format(d))
            # print('Position previous: \n{0}'.format(prev_position))
            # print('Position current: \n{0}'.format(pos_rec))


            transactions = self._calc_transactions(d, pos_rec, prev_position)
            # print("Transactions: \n{0}".format(transactions))

            for contract_hash, qty in transactions.items():
                if qty == 0:
                    continue

                contract = datasource.get(contract_hash, decision_time_end)
                position.add(Transaction(contract, decision_time_end, qty))

                if isinstance(contract, FutureContract):
                    costs_sum += -abs(costs_per_contract) * abs(qty)
                else:
                    costs_sum += -abs(costs_per_option) * abs(qty)

            try:
                pnl = position.pnl_settlement + costs_sum
            except:
                pnl = float('nan')
            # print("Pnl: {0}".format(pnl))
            prev_position = pos_rec

            p_dict = position.as_dict()
            account_pnl.append(pnl)
            account_pnl_index.append(d)
            costs.append(costs_sum)

        return pd.DataFrame({
            'SettleChange': pd.Series(account_pnl, index=account_pnl_index).diff(),
            'Costs': pd.Series(costs, index=account_pnl_index)
        }
        )

    def run_compare_report(self, campaign_stats, num_days_back, office, account):
        import matplotlib.pyplot as plt
        model_tail = pd.DataFrame(campaign_stats['SettleChange'].tail(num_days_back))

        model_tail['Model_Equity'] = pd.DataFrame(
            campaign_stats['SettleChange'].tail(num_days_back)).ffill().cumsum(axis=0)

        model_tail['Model_Costs'] = pd.DataFrame(campaign_stats['Costs'].tail(num_days_back))

        start_date = model_tail.index[0].strftime('%Y-%m-%d')

        col_s = self.collection.find(
            {'Batchid': {'$gte': start_date},
             'Office': office, 'Account': account, 'SummaryDetailFlag': 'S', 'AccountType': '9Z'})

        col_d = self.collection.find(
            {'Batchid': {'$gte': start_date},
             'Office': office, 'Account': account, 'SummaryDetailFlag': 'D'})
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


if __name__ == '__main__':
    from backtester.reports.campaign_report import CampaignReport
    from exobuilder.contracts.futurecontract import FutureContract
    from datetime import datetime
    from exobuilder.data.datasource_mongo import DataSourceMongo
    from exobuilder.data.assetindex_mongo import AssetIndexMongo
    from exobuilder.data.exostorage import EXOStorage
    from exobuilder.exo.transaction import Transaction

    assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
    storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

    futures_limit = 3
    options_limit = 10

    num_of_days_back_master = 10

    # datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, assetindex, futures_limit, options_limit, storage)
    datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, futures_limit, options_limit, storage)

    rpt = CampaignReport('ES_Bidirectional V3', datasource, pnl_settlement_ndays=num_of_days_back_master + 1)

    crc = CampaignRealCompare()
    archive_based_pnl = crc.get_account_positions_archive_pnl(account_name="CLX60125",
                                                              instrument="ES",
                                                              # costs_per_contract=3.0 # Default
                                                              # costs_per_option=3.0 # Default
                                                              num_days_back=num_of_days_back_master + 1
                                                              )

    pass