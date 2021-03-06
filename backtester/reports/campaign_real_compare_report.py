from collections import OrderedDict

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
from pymongo import MongoClient
from backtester.reports.campaign_report import CampaignReport
from exobuilder.contracts.futurecontract import FutureContract
from datetime import datetime
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.exostorage import EXOStorage
from exobuilder.exo.transaction import Transaction
from exobuilder.exo.position import Position
from scripts.settings import *
import warnings
import pickle
import lz4


class CampaignRealCompare:
    def __init__(self):
        tmp_mongo_connstr = 'mongodb://tmqr:tmqr@10.0.1.2/client-gmi?authMechanism=SCRAM-SHA-1'
        tmp_mongo_db = 'client-gmi'

        mongoClient = MongoClient(tmp_mongo_connstr)
        db = mongoClient[tmp_mongo_db]
        self.collection = db.accountsummarycollection

    @staticmethod
    def _calc_transactions(date, current_pos, prev_pos, idinstrument=None):
        result = {}
        assert current_pos is not None, 'current_pos must be initialized'

        if prev_pos is None:
            intersected_assets = set(current_pos)
        else:
            intersected_assets = set(current_pos) | set(prev_pos)

        for asset in intersected_assets:
            prev_values = prev_pos.get(asset, None) if prev_pos is not None else None
            curr_values = current_pos.get(asset, None)

            if idinstrument is not None:
                if prev_values is not None and prev_values['idinstrument'] != idinstrument:
                    continue
                if curr_values is not None and curr_values['idinstrument'] != idinstrument:
                    continue

            if prev_values is None:
                result[asset] = curr_values['qty']
            elif curr_values is None:
                # Skip old closed positions
                if prev_values['qty'] != 0:
                    result[asset] = -prev_values['qty']
            else:
                # Calculating transactions for existing position
                trans_qty = curr_values['qty'] - prev_values['qty']

                result[asset] = trans_qty
        return result

    def get_account_positions_archive_pnl(self, account_name=None, instrument=None, costs_per_option=3.0,
                                          costs_per_contract=3.0,
                                          num_days_back=20, fcm_office=None, fcm_acct=None, return_transactions=False):

        mongoClient = MongoClient(MONGO_CONNSTR)
        db = mongoClient[MONGO_EXO_DB]

        storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, 4, 20, storage)

        position_dict = OrderedDict()

        transactions_dict = {}

        if account_name is None:

            account = db['accounts'].find_one({'FCM_OFFICE': fcm_office, 'FCM_ACCT': fcm_acct})

            if account is None:
                raise KeyError("Account is not found. FCM_OFFICE:{0} FCM_ACCT:{1}".format(fcm_office, fcm_acct))

            account_name = account['name']

        reversedList = reversed(list(
            db['accounts_positions_archive'].find({'name': account_name}).sort([('date_now', -1)]).limit(
                num_days_back)))

        for pos in reversedList:
            # print(pos)

            dt = pos['date_now']
            pos_rec = position_dict.setdefault(dt, {})

            for p in pos['positions']:
                if '_hash' not in p['asset']:
                    break

                # pos_rec[p['asset']['_hash']] = p['qty']
                pos_rec[p['asset']['_hash']] = {'qty': p['qty'], 'idinstrument': p['asset']['idinstrument']}

        prev_position = None

        account_pnl = []
        costs = []
        account_pnl_index = []

        p_dict = Position().as_dict()

        for d, pos_rec in position_dict.items():
            costs_sum = 0.0
            pnl = 0.0

            asset_info = assetindex.get_instrument_info(instrument)

            daily_transactions_list = transactions_dict.setdefault(d, [])

            if prev_position is not None:
                position = Position.from_dict(p_dict, datasource, decision_time_end)

                new_exec_time_end, new_decision_time_end = AssetIndexMongo.get_exec_time(d, asset_info)
                try:
                    tmp_prev_pnl = position.pnl_settlement
                    position.set_date(datasource, new_decision_time_end)

                    pnl = position.pnl_settlement - tmp_prev_pnl
                except Exception as exc:
                    pnl = float('nan')
                    warnings.warn("Error getting settlements: {0}".format(exc))

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
                trans_ = Transaction(contract, decision_time_end, qty)

                daily_transactions_list.append(trans_)
                position.add(trans_)

                if isinstance(contract, FutureContract):
                    costs_sum += -abs(costs_per_contract) * abs(qty)
                else:
                    costs_sum += -abs(costs_per_option) * abs(qty)

            pnl += costs_sum
            # print("Pnl: {0}".format(pnl))
            prev_position = pos_rec

            p_dict = position.as_dict()
            account_pnl.append(pnl)
            account_pnl_index.append(d)
            costs.append(costs_sum)

        if return_transactions:
            return pd.DataFrame({
                'SettleChange': pd.Series(account_pnl, index=account_pnl_index),
                'Costs': pd.Series(costs, index=account_pnl_index)
            }
            ), transactions_dict
        else:
            return pd.DataFrame({
                'SettleChange': pd.Series(account_pnl, index=account_pnl_index),
                'Costs': pd.Series(costs, index=account_pnl_index)
            }
            )

    def get_account_positions_archive_pnl_multiproduct(self, account_name=None, instrument=None, costs_per_option=3.0,
                                                       costs_per_contract=3.0,
                                                       num_days_back=20, fcm_office=None, fcm_acct=None,
                                                       return_transactions=False):

        mongoClient = MongoClient(MONGO_CONNSTR)
        db = mongoClient[MONGO_EXO_DB]

        storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, 4, 20, storage)

        position_dict = OrderedDict()

        if account_name is None:

            account = db['accounts'].find_one({'FCM_OFFICE': fcm_office, 'FCM_ACCT': fcm_acct})

            if account is None:
                raise KeyError("Account is not found. FCM_OFFICE:{0} FCM_ACCT:{1}".format(fcm_office, fcm_acct))

            account_name = account['name']

        reversedList = reversed(list(
            db['accounts_positions_archive'].find({'name': account_name}).sort([('date_now', -1)]).limit(
                num_days_back)))

        instrument_id_set = set()
        instrument_info_dict = {}

        for pos in reversedList:
            # print(pos)

            dt = pos['date_now']
            pos_rec = position_dict.setdefault(dt, {})

            for p in pos['positions']:
                if '_hash' not in p['asset']:
                    break

                instrument_id_set.add(p['asset']['idinstrument'])

                pos_rec[p['asset']['_hash']] = {'qty': p['qty'], 'idinstrument': p['asset']['idinstrument']}

        # Setting up instruments
        for _ins_id in instrument_id_set:
            instrument_info_dict[_ins_id] = {
                'instrument_info': assetindex.get_instrument_info(idinstrument=_ins_id),
                'prev_position': None,
                'account_pnl': [],
                'costs': [],
                'account_pnl_index': [],
                'p_dict': Position().as_dict(),
                'decision_time_end': None,
                'exec_time_end': None,
                'transactions_dict': OrderedDict(),
            }

        for d, pos_rec in position_dict.items():
            for instr, instr_values in instrument_info_dict.items():
                costs_sum = 0.0
                pnl = 0.0

                asset_info = instr_values['instrument_info']

                daily_transactions_list = instr_values['transactions_dict'].setdefault(d, [])

                if instr_values['prev_position'] is not None:
                    position = Position.from_dict(instr_values['p_dict'], datasource, instr_values['decision_time_end'])

                    new_exec_time_end, new_decision_time_end = AssetIndexMongo.get_exec_time(d, asset_info)

                    try:
                        tmp_prev_pnl = position.pnl_settlement
                        position.set_date(datasource, new_decision_time_end)
                        pnl = position.pnl_settlement - tmp_prev_pnl
                    except Exception as exc:
                        pnl = float('nan')
                        warnings.warn("Error getting settlements: {0}".format(exc))

                instr_values['exec_time_end'], instr_values['decision_time_end'] = AssetIndexMongo.get_exec_time(d,
                                                                                                                 asset_info)

                position = Position.from_dict(instr_values['p_dict'], datasource, instr_values['decision_time_end'])

                transactions = self._calc_transactions(d, pos_rec, instr_values['prev_position'], idinstrument=instr)

                for contract_hash, qty in transactions.items():
                    if qty == 0:
                        continue

                    contract = datasource.get(contract_hash, instr_values['decision_time_end'])

                    assert contract.instrument.dbid == instr

                    trans_ = Transaction(contract, instr_values['decision_time_end'], qty)

                    daily_transactions_list.append(trans_)
                    position.add(trans_)

                    if isinstance(contract, FutureContract):
                        costs_sum += -abs(costs_per_contract) * abs(qty)
                    else:
                        costs_sum += -abs(costs_per_option) * abs(qty)

                pnl += costs_sum
                # print("Pnl: {0}".format(pnl))
                instr_values['prev_position'] = pos_rec

                instr_values['p_dict'] = position.as_dict()
                instr_values['account_pnl'].append(pnl)
                instr_values['account_pnl_index'].append(d)
                instr_values['costs'].append(costs_sum)
        pass

        result = {}
        for instr, instr_values in instrument_info_dict.items():
            result[instr_values['instrument_info']['exchangesymbol']] = {
                'pnls': pd.DataFrame({
                    'SettleChange': pd.Series(instr_values['account_pnl'], index=instr_values['account_pnl_index']),
                    'Costs': pd.Series(instr_values['costs'], index=instr_values['account_pnl_index'])
                }),
                'transactions': instr_values['transactions_dict']
            }

        return result

    def get_account_positions_archive_pnl_multiproduct_no_trans(self, account_name=None, instrument=None, costs_per_option=3.0,
                                                       costs_per_contract=3.0,
                                                       num_days_back=2, fcm_office=None, fcm_acct=None,
                                                       return_transactions=False):

        mongoClient = MongoClient(MONGO_CONNSTR)
        db = mongoClient[MONGO_EXO_DB]

        storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
        datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, 4, 20, storage)

        position_dict = OrderedDict()

        if account_name is None:

            account = db['accounts'].find_one({'FCM_OFFICE': fcm_office, 'FCM_ACCT': fcm_acct})

            if account is None:
                raise KeyError("Account is not found. FCM_OFFICE:{0} FCM_ACCT:{1}".format(fcm_office, fcm_acct))

            account_name = account['name']

        reversedList = reversed(list(
            db['accounts_positions_archive_copy'].find({'name': account_name}).sort([('date_now', -1)]).limit(
                num_days_back)))

        instrument_id_set = set()
        instrument_info_dict = {}
        instrument_info_dict_current_day = {}

        for pos in reversedList:
            # print(pos)

            dt = pos['date_now']
            pos_rec = position_dict.setdefault(dt, {})

            for p in pos['positions']:
                if '_hash' not in p['asset']:
                    break

                instrument_id_set.add(p['asset']['idinstrument'])

                pos_rec[p['asset']['_hash']] = {'qty': p['qty'], 'idinstrument': p['asset']['idinstrument']}

        # Setting up instruments
        for _ins_id in instrument_id_set:
            instrument_info_dict[_ins_id] = {
                'instrument_info': assetindex.get_instrument_info(idinstrument=_ins_id),
                'prev_position': None,
                'account_pnl': [],
                'costs': [],
                'account_pnl_index': [],
                'p_dict': Position().as_dict(),
                'decision_time_end': None,
                'exec_time_end': None,
                'transactions_dict': OrderedDict(),
            }

            instrument_info_dict_current_day[_ins_id] = {
                'instrument_info': assetindex.get_instrument_info(idinstrument=_ins_id),
                'prev_position': None,
                'account_pnl': [],
                'costs': [],
                'account_pnl_index': [],
                'p_dict': Position().as_dict(),
                'decision_time_end': None,
                'exec_time_end': None,
                'transactions_dict': OrderedDict(),
            }



        for d, pos_rec in position_dict.items():

            instrument_info = db['accounts_positions_archive_copy'].find_one({'name': account_name, 'date_now': d})

            if 'position_by_instrument' in instrument_info:
                mongo_unpickled_position = pickle.loads(lz4.block.decompress(instrument_info['position_by_instrument']))

                for instr, instr_values in instrument_info_dict.items():
                    # instrument_info_dict_current_day[instr]['prev_position'] = pos_rec
                    # instrument_info_dict_current_day[instr]['p_dict'] = position.as_dict()
                    # instrument_info_dict_current_day[instr]['account_pnl'] = pnl
                    # instrument_info_dict_current_day[instr]['account_pnl_index'] = d
                    # instrument_info_dict_current_day[instr]['costs'] = costs_sum
                    # instrument_info_dict_current_day[instr]['transactions_dict'] = daily_transactions_list_dt.as_dict()
                    # **********************

                    instr_values['prev_position'] = mongo_unpickled_position[instr]['prev_position']
                    instr_values['p_dict'] = mongo_unpickled_position[instr]['p_dict']
                    instr_values['account_pnl'].append(mongo_unpickled_position[instr]['account_pnl'])
                    instr_values['account_pnl_index'].append(mongo_unpickled_position[instr]['account_pnl_index'])
                    instr_values['costs'].append(mongo_unpickled_position[instr]['costs'])

            else:
                for instr, instr_values in instrument_info_dict.items():
                    costs_sum = 0.0
                    pnl = 0.0

                    asset_info = instr_values['instrument_info']

                    daily_transactions_list = instr_values['transactions_dict'].setdefault(d, [])

                    daily_transactions_list_dt = []

                    if instr_values['prev_position'] is not None:
                        position = Position.from_dict(instr_values['p_dict'], datasource, instr_values['decision_time_end'])

                        new_exec_time_end, new_decision_time_end = AssetIndexMongo.get_exec_time(d, asset_info)

                        try:
                            tmp_prev_pnl = position.pnl_settlement
                            position.set_date(datasource, new_decision_time_end)
                            pnl = position.pnl_settlement - tmp_prev_pnl
                        except Exception as exc:
                            pnl = float('nan')
                            warnings.warn("Error getting settlements: {0}".format(exc))

                    instr_values['exec_time_end'], instr_values['decision_time_end'] = AssetIndexMongo.get_exec_time(d,
                                                                                                                     asset_info)

                    position = Position.from_dict(instr_values['p_dict'], datasource, instr_values['decision_time_end'])

                    transactions = self._calc_transactions(d, pos_rec, instr_values['prev_position'], idinstrument=instr)

                    for contract_hash, qty in transactions.items():
                        if qty == 0:
                            continue

                        contract = datasource.get(contract_hash, instr_values['decision_time_end'])

                        assert contract.instrument.dbid == instr

                        trans_ = Transaction(contract, instr_values['decision_time_end'], qty)

                        daily_transactions_list_dt.append(trans_)
                        daily_transactions_list.append(trans_)
                        position.add(trans_)

                        if isinstance(contract, FutureContract):
                            costs_sum += -abs(costs_per_contract) * abs(qty)
                        else:
                            costs_sum += -abs(costs_per_option) * abs(qty)

                    pnl += costs_sum
                    # print("Pnl: {0}".format(pnl))
                    #**********************
                    instrument_info_dict_current_day[instr]['prev_position'] = pos_rec
                    instrument_info_dict_current_day[instr]['p_dict'] = position.as_dict()
                    instrument_info_dict_current_day[instr]['account_pnl'] = pnl
                    instrument_info_dict_current_day[instr]['account_pnl_index'] = d
                    instrument_info_dict_current_day[instr]['costs'] = costs_sum
                    # instrument_info_dict_current_day[instr]['transactions_dict'] = daily_transactions_list_dt.as_dict()
                    #**********************

                    instr_values['prev_position'] = pos_rec

                    instr_values['p_dict'] = position.as_dict()
                    instr_values['account_pnl'].append(pnl)
                    instr_values['account_pnl_index'].append(d)
                    instr_values['costs'].append(costs_sum)


                mongo_input = lz4.block.compress(pickle.dumps(instrument_info_dict_current_day))
                db['accounts_positions_archive_copy'].update_one({'name': account_name, 'date_now': d},
                                                                 {'$set': {'position_by_instrument': mongo_input}})

                # instrument_info = db['accounts_positions_archive_copy'].find_one({'name': account_name, 'date_now': d})
                #
                # mongo_input = pickle.loads(lz4.block.decompress(instrument_info['instrument_info']))

        pass






        result = {}
        for instr, instr_values in instrument_info_dict.items():
            result[instr_values['instrument_info']['exchangesymbol']] = {
                'pnls': pd.DataFrame({
                    'SettleChange': pd.Series(instr_values['account_pnl'], index=instr_values['account_pnl_index']),
                    'Costs': pd.Series(instr_values['costs'], index=instr_values['account_pnl_index'])
                })
                #, 'transactions': instr_values['transactions_dict']
            }

        return result

    def run_compare_report(self, campaign_stats, num_days_back, office, account):

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

        if not tail_table_cost_real.empty:
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

        if not tail_plot_real.empty:
            tail_plot_real.index = tail_plot_real['date']
            del tail_plot_real['date']
            tail_plot_real['Model_Equity'] = model_tail['Model_Equity'] + tail_plot_real['Real_Equity'][0]
        else:
            tail_plot_real['Model_Equity'] = model_tail['Model_Equity']

        tail_table_real = pd.DataFrame(table_series)

        if not tail_table_real.empty:
            tail_table_real.index = tail_table_real['date']
            del tail_table_real['date']

        tail_table_real['Model_Equity'] = model_tail['Model_Equity']
        tail_table_real['Model_Change'] = model_tail['SettleChange']

        if not tail_table_cost_real.empty:
            tail_table_real['Real_Buys'] = tail_table_cost_real['TradedQuantityBuy']
            tail_table_real['Real_Sells'] = tail_table_cost_real['TradedQuantitySell']
            tail_table_real['Real_Costs'] = tail_table_cost_real['Real_Costs']
        else:
            tail_table_real['Real_Buys'] = 0
            tail_table_real['Real_Sells'] = 0
            tail_table_real['Real_Costs'] = 0

        tail_table_real['Model_Costs'] = model_tail['Model_Costs']

        sum_row = tail_table_real.sum(axis=0)
        print(sum_row)

        # print( tail_table_real)
        # tail_table_real=tail_table_real.append(sum_row)
        print(tail_table_real)
        print('Total_Real_Buys', sum_row['Real_Buys'])
        print('Total_Real_Sells', sum_row['Real_Sells'])
        print('Total_Real_Costs', sum_row['Real_Costs'])
        print('Total_Model_Costs', sum_row['Model_Costs'])

        tail_plot_real.plot()  # ax=ax1,label='At expiration', lw=2, c='blue');
        #         model_tail.plot()
        plt.show()

    def run_return_report(self, office, account, initial_acct_value=50000):

        col_s = self.collection.find(
            {'Office': office, 'Account': account, 'SummaryDetailFlag': 'S', 'AccountType': '9Z'})

        series = []
        table_series = []
        cumValue = 0
        for post_s in col_s:
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

        returns = pd.DataFrame()

        if not tail_plot_real.empty:
            tail_plot_real.index = tail_plot_real['date']
            del tail_plot_real['date']

            tail_plot_real.plot()  # ax=ax1,label='At expiration', lw=2, c='blue');
            plt.show()

            x = tail_plot_real['Real_Equity']
            calc_daily_dollar_change = np.subtract(x[1:], x[0:-1])
            tail_plot_real['Daily_Dollar_Change'] = calc_daily_dollar_change

            sample = pd.DataFrame()
            sample['Real_Equity'] = tail_plot_real.Real_Equity.resample('M').last() + initial_acct_value
            sample['Dollar_Change'] = tail_plot_real.Daily_Dollar_Change.resample('M').sum()
            sample['Real_Equity_Percent_Change'] = (sample['Real_Equity'].pct_change() * 100).apply('{:,.2f}%'.format)
            print(sample)

            minyear = min(sample.index.year)
            maxyear = max(sample.index.year)

            row_headers = list(range(minyear, maxyear + 1))
            #             returns = pd.DataFrame()

            returns['year'] = row_headers

            for i in range(1, 13):
                returns[calendar.month_name[i]] = ''

            returns = returns.set_index('year')

            for years in row_headers:
                for months in range(1, 13):
                    if len(sample['Real_Equity_Percent_Change'][
                                       (sample.index.month == months) & (sample.index.year == years)].index) != 0:
                        returns.ix[years][calendar.month_name[months]] = sample['Real_Equity_Percent_Change'][
                            (sample.index.month == months) & (sample.index.year == years)].item()

        return returns

if __name__ == '__main__':
    assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
    storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

    futures_limit = 3
    options_limit = 10

    num_of_days_back_master = 2

    # datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, assetindex, futures_limit, options_limit, storage)
    datasource = DataSourceMongo(MONGO_CONNSTR, MONGO_EXO_DB, assetindex, futures_limit, options_limit, storage)

    #rpt = CampaignReport('ES_Bidirectional V3', datasource, pnl_settlement_ndays=num_of_days_back_master + 1)

    crc = CampaignRealCompare()
    archive_based_pnl = crc.get_account_positions_archive_pnl_multiproduct_no_trans(#account_name="CLX60125",
                                                               instrument="CL",
                                                              # costs_per_contract=3.0 # Default
                                                              # costs_per_option=3.0 # Default
                                                              num_days_back=num_of_days_back_master + 1,
                                                              fcm_office="TEST", fcm_acct="SC_DIV_NO_GC_1"
                                                              )

    print(archive_based_pnl)

    pass
