from datetime import datetime, timedelta
import pickle
from collections import OrderedDict
import pandas as pd
from exobuilder.data.exceptions import QuoteNotFoundException
import warnings
from tradingcore.campaign import Campaign
from exobuilder.data.assetindex_mongo import AssetIndexMongo
import os, sys
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.exceptions import QuoteNotFoundException
import matplotlib.pyplot as plt

#
# Warnings messages formatting
#
def custom_formatwarning(msg, *a):
    # ignore everything except the message
    return str(msg) + '\n'
warnings.formatwarning = custom_formatwarning

def ipython_info():
    ip = False
    if 'ipykernel' in sys.modules:
        ip = 'notebook'
    elif 'IPython' in sys.modules:
        ip = 'terminal'
    return ip


COMMISSION_PER_CONTRACT = 3.0


class CampaignReport:
    def __init__(self, campaign_name, datasource=None, **kwargs):
        self.datasource = datasource

        storage = kwargs.get('exo_storage', False)
        raise_exc = kwargs.get('raise_exceptions', False)

        self.pnl_settlement_ndays = kwargs.get('pnl_settlement_ndays', 10)

        if not storage:
            storage = self.datasource.exostorage
            calc_settlements = True
        else:
            calc_settlements = False

        campaign_dict = storage.campaign_load(campaign_name)
        if campaign_dict is None:
            if raise_exc:
                raise Exception("Campaign not found: " + campaign_name)
            else:
                warnings.warn("Campaign not found: " + campaign_name)
            return
        self.last_date = None
        self.prev_date = None

        self.cmp = Campaign(campaign_dict, self.datasource)
        self.campaign_name = campaign_name
        self.swarms_data = storage.swarms_data(self.cmp.alphas_list())
        self.isok = True

        campaign_dict = {}
        campaign_deltas_dict = {}
        campaign_costs_dict = {}

        swm_data = storage.swarms_data(self.cmp.alphas_list())

        for alpha_name, swm_exposure_dict in self.cmp.alphas.items():
            swarm_name = alpha_name
            series = swm_data[swarm_name]['swarm_series']

            date_begin = swm_exposure_dict.get('begin', datetime(1900, 1, 1))
            date_end = swm_exposure_dict.get('end', datetime(2100, 1, 1))

            campaign_dict[swarm_name] = series['equity'].ix[date_begin:date_end] * swm_exposure_dict['qty']
            campaign_deltas_dict[swarm_name] = series['delta'].ix[date_begin:date_end] * swm_exposure_dict['qty']
            campaign_costs_dict[swarm_name] = series['costs'].ix[date_begin:date_end] * swm_exposure_dict['qty']


        campaign_equity = pd.DataFrame(campaign_dict).ffill().sum(axis=1)
        campaign_deltas = pd.DataFrame(campaign_deltas_dict).sum(axis=1)
        campaign_costs = pd.DataFrame(campaign_costs_dict).sum(axis=1)

        result_dict = {
            'Equity': campaign_equity,
            'Change': campaign_equity.diff(),
            'Delta': campaign_deltas,
            'Costs': campaign_costs
        }
        if calc_settlements:
            campaign_settle_chg = pd.Series(index=campaign_equity.index)
            prev_idx_dt = None
            for idx_dt in campaign_settle_chg.index[-self.pnl_settlement_ndays:]:
                if prev_idx_dt is None:
                    prev_idx_dt = idx_dt
                    continue
                try:
                    diff = self.cmp.positions_at_date(prev_idx_dt, idx_dt).pnl_settlement - self.cmp.positions_at_date(
                                                                                                    prev_idx_dt).pnl_settlement
                except QuoteNotFoundException:
                    diff = float('nan')


                campaign_settle_chg[idx_dt] = diff + campaign_costs[idx_dt]
                prev_idx_dt = idx_dt
            result_dict['SettleChange'] = campaign_settle_chg

        self.campaign_stats = pd.DataFrame(result_dict)

    def check_swarms_integrity(self):
        isok = True
        last_date = datetime(1900, 1, 1)
        prev_date = datetime(1900, 1, 1)
        decision_time = datetime(1900, 1, 1, 0, 0, 0)
        instrument_name = None

        for k, v in self.swarms_data.items():
            seriesdf = v['swarm_series']
            last_date = max(last_date, seriesdf.index[-1])
            prev_date = max(prev_date, seriesdf.index[-2])

        for k, v in self.swarms_data.items():
            # Skip integrity checks for inactive alphas
            if not self.cmp.alpha_is_active(k, last_date):
                continue
            instrument = k.split('_')[0]
            seriesdf = v['swarm_series']
            asset_info = self.datasource.assetindex.get_instrument_info(instrument)
            exec_time, decision_time = AssetIndexMongo.get_exec_time(datetime.now(), asset_info)


            if instrument_name is None:
                instrument_name = instrument
            else:
                if instrument_name != instrument:
                    raise ValueError("The campaign has different products, only mono-product campaigns are supported")

            if (last_date - v['last_date']).days > 0:
                warnings.warn('[DELAYED] {0}: {1}'.format(k, v['last_date']))
                isok = False
            elif datetime.now() > decision_time and (datetime.now() - v['last_date']).days > 0:
                warnings.warn('[NOT_ACTUAL] {0}: {1}'.format(k, v['last_date']))
                isok = False
            elif (prev_date - seriesdf.index[-2]).days > 0:
                warnings.warn('[ERR_PREVDAY] {0}: {1}'.format(k, seriesdf.index[-2]))
                isok = False

        print('Last quote date: {0} Pevious date: {1}'.format(last_date, prev_date))

        if isok:
            print('Alphas seems to be valid')
        else:
            warnings.warn("Some alphas corrupted!")

        self.last_date = datetime.combine(last_date.date(), decision_time.time())
        self.prev_date = datetime.combine(prev_date.date(), decision_time.time())

        return isok

    def report_exo_exposure(self):
        exos = OrderedDict()

        for exo_name, exp_dict in self.cmp.exo_positions(self.last_date).items():
            edic = exos.setdefault(exo_name, {'LastDate': 0.0, 'PrevDate': 0.0})
            edic['LastDate'] = exp_dict['exposure']

        for exo_name, exp_dict in self.cmp.exo_positions(self.prev_date).items():
            edic = exos.setdefault(exo_name, {'LastDate': 0.0, 'PrevDate': 0.0})
            edic['PrevDate'] = exp_dict['exposure']

        print("\n\nEXO Exposure report")
        print(pd.DataFrame(exos).T.sort_index())

    def report_alpha_exposure(self):
        pd.set_option('display.max_colwidth', 90)
        pd.set_option('display.width', 1000)

        alphas = OrderedDict()
        for alpha_name, exp_dict in self.cmp.alphas_positions(self.last_date).items():
            edic = alphas.setdefault(alpha_name, {'LastDate': 0.0, 'PrevDate': 0.0})
            edic['LastDate'] = exp_dict['exposure']

        for alpha_name, exp_dict in self.cmp.alphas_positions(self.prev_date).items():
            edic = alphas.setdefault(alpha_name, {'LastDate': 0.0, 'PrevDate': 0.0})
            edic['PrevDate'] = exp_dict['exposure']

        print("\n\nAlphas Exposure report")
        print(pd.DataFrame(alphas).T.sort_index())

    def report_positions(self):
        pos_last = self.cmp.positions_at_date(self.last_date)
        pos_prev = self.cmp.positions_at_date(self.prev_date)
        pos_prev_pnl = self.cmp.positions_at_date(self.prev_date, self.last_date)

        positions = OrderedDict()
        for contract, exp_dict in pos_last.netpositions.items():
            try:
                edic = positions.setdefault(contract.name, {'LastDate': 0.0, 'PrevDate': 0.0, 'Contract': contract})
                edic['LastDate'] = exp_dict['qty']
            except QuoteNotFoundException:
                warnings.warn("QuoteNotFound for: {0}".format(contract.name))

        for contract, exp_dict in pos_prev.netpositions.items():
            try:
                edic = positions.setdefault(contract.name, {'LastDate': 0.0, 'PrevDate': 0.0, 'Contract': contract})
                edic['PrevDate'] = exp_dict['qty']
            except QuoteNotFoundException:
                warnings.warn("QuoteNotFound for: {0}".format(contract.name))

        print("\n\nPositions Exposure report")
        df = pd.DataFrame(positions).T.sort_index()
        if len(df) > 0:
            print(df[['LastDate', 'PrevDate']])
        else:
            print('No positions opened')

        print("\nTrades report")
        if len(df) > 0:
            df['Qty'] = df['LastDate'] - df['PrevDate']
            df['Price'] = df['Contract'].apply(lambda x: x.price)
            trades_df = df[df['Qty'] != 0]
            if len(trades_df) > 0:
                print(trades_df[['Qty', 'Price']])
            else:
                print("No trades occurred")
        else:
            print("No trades occurred")

    def report_pnl(self):
        print(self.campaign_stats.tail(self.pnl_settlement_ndays))

    def report_export(self):
        from IPython.display import display, HTML

        if not os.path.exists('export'):
            os.mkdir('export')

        if not os.path.exists(os.path.join('export', 'campaigns')):
            os.mkdir(os.path.join('export', 'campaigns'))

        fn = os.path.join('export', 'campaigns', self.campaign_name + '.csv')
        self.campaign_stats.to_csv(fn)

        if ipython_info() == 'notebook':
            link = '<a href="{0}" target="_blank">Download CSV: {1}</a>'.format(fn, self.campaign_name)
            display(HTML(link))
        else:
            print("File saved to: {0}".format(fn))

    def calculate_performance_fee(self, starting_capital=50000, dollar_costs=3, performance_fee=0.2, fixed_mgmt_fee=0, plot_graph=False):
            eq = self.campaign_stats.Equity
            costs_sum = self.campaign_stats['Costs'].cumsum()
            equity_without_costs = (eq - costs_sum)

            #
            # Calculating equity with new costs
            #
            ncontracts_traded = (self.campaign_stats['Costs'] / 3.0).abs()
            new_costs = ncontracts_traded * -abs(dollar_costs)
            new_equity = equity_without_costs + new_costs.cumsum() + starting_capital

            #
            # Calculation of the performance fees (with high-water mark)
            #
            monthly_eq = new_equity.resample('M').last()
            monthly_high_watermark = monthly_eq.expanding().max().shift()

            # Skip periods when equity closed lower than previous month's high-water mark
            performance_fee_base = monthly_eq - monthly_high_watermark
            performance_fee_base[performance_fee_base <= 0] = 0
            performance_fee = performance_fee_base * -abs(performance_fee)

            management_fee = pd.Series(-abs(fixed_mgmt_fee), index=performance_fee.index)

            performance_fees_sum = performance_fee.cumsum().reindex(eq.index, method='ffill')
            management_fee_sum = management_fee.cumsum().reindex(eq.index, method='ffill')
            performance_fee_equity = new_equity + performance_fees_sum + management_fee_sum

            df_result = pd.DataFrame({
                "equity_original": eq + starting_capital,
                "equity_with_costs": new_equity,
                "equity_all_included": performance_fee_equity,
                "costs_sum": new_costs.cumsum(),
                'performance_fee_sum': performance_fees_sum,
                'management_fee_sum': management_fee_sum,
            })

            if plot_graph:
                df_result[["equity_original", "equity_with_costs", "equity_all_included"]].plot()
                plt.figure()
                df_result[["costs_sum", 'performance_fee_sum', 'management_fee_sum']].plot()
            return df_result

    def report_all(self):
        self.check_swarms_integrity()
        self.report_exo_exposure()
        self.report_alpha_exposure()
        self.report_positions()
        self.report_pnl()
        self.report_export()

if __name__ == '__main__':
    from scripts.settings import *
    # from backtester.reports.campaign_report import CampaignReport
    from exobuilder.data.assetindex_mongo import AssetIndexMongo
    from exobuilder.data.datasource_sql import DataSourceSQL
    from exobuilder.data.exostorage import EXOStorage

    assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
    storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
    datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, assetindex, 3, 20, storage)

    rpt = CampaignReport('ES_Collect_V1', datasource)
    rpt.report_all()