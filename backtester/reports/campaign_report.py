from datetime import datetime, timedelta
import pickle
from collections import OrderedDict
import pandas as pd
from exobuilder.data.exceptions import QuoteNotFoundException
import warnings
from tradingcore.campaign import Campaign
from exobuilder.data.assetindex_mongo import AssetIndexMongo


class CampaignReport:
    def __init__(self, campaign_name, datasource):
        self.datasource = datasource
        campaign_dict = self.datasource.exostorage.campaign_load(campaign_name)
        if campaign_dict is None:
            warnings.warn("Campaign not found: " + campaign_name)
            return
        self.last_date = None
        self.prev_date = None

        self.cmp = Campaign(campaign_dict, self.datasource)
        self.swarms_data = datasource.exostorage.swarms_data(self.cmp.alphas_list())
        self.isok = self.check_swarms_integrity()

    def check_swarms_integrity(self):
        isok = True
        last_date = datetime(1900, 1, 1)
        prev_date = datetime(1900, 1, 1)
        decision_time = None
        instrument_name = None

        for k, v in self.swarms_data.items():
            seriesdf = v['swarm_series']
            last_date = max(last_date, seriesdf.index[-1])
            prev_date = max(prev_date, seriesdf.index[-2])

        for k, v in self.swarms_data.items():
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
                print('[DELAYED] {0}: {1}'.format(k, v['last_date']))
                isok = False
            elif datetime.now() > decision_time and (datetime.now() - v['last_date']).days > 0:
                print('[NOT_ACTUAL] {0}: {1}'.format(k, v['last_date']))
                isok = False
            elif (prev_date - seriesdf.index[-2]).days > 0:
                print('[ERR_PREVDAY] {0}: {1}'.format(k, seriesdf.index[-2]))
                isok = False

        print('Last quote date: {0} Pevious date: {1}'.format(last_date, prev_date))

        if isok:
            print('Alphas seems to be valid')
        else:
            print("Some alphas corrupted!")

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
                print("QuoteNotFound for: {0}".format(contract.name))

        for contract, exp_dict in pos_prev.netpositions.items():
            try:
                edic = positions.setdefault(contract.name, {'LastDate': 0.0, 'PrevDate': 0.0, 'Contract': contract})
                edic['PrevDate'] = exp_dict['qty']
            except QuoteNotFoundException:
                print("QuoteNotFound for: {0}".format(contract.name))

        print("\n\nPositions Exposure report")
        df = pd.DataFrame(positions).T.sort_index()
        print(df[['LastDate', 'PrevDate']])

        print("\nTrades report")
        df['Qty'] = df['LastDate'] - df['PrevDate']
        df['Price'] = df['Contract'].apply(lambda x: x.price)
        trades_df = df[df['Qty'] != 0]
        if len(trades_df) > 0:
            print(trades_df[['Qty', 'Price']])
        else:
            print("No trades occurred")

        print("\nPnL between decision moments (without costs)\n"
              "[{0} - {1}]:{2: 0.2f}".format(self.prev_date,
                                       self.last_date,
                                       pos_prev_pnl.pnl - pos_prev.pnl))

    def report_pnl(self):
        campaign_dict = {}
        campaign_deltas_dict = {}
        campaign_costs_dict = {}

        swm_data = self.datasource.exostorage.swarms_data(self.cmp.alphas_list())

        for alpha_name, swm_exposure_dict in self.cmp.alphas.items():
            swarm_name = alpha_name
            series = swm_data[swarm_name]['swarm_series']
            campaign_dict[swarm_name] = series['equity'] * swm_exposure_dict['qty']
            campaign_deltas_dict[swarm_name] = series['delta'] * swm_exposure_dict['qty']
            campaign_costs_dict[swarm_name] = series['costs'] * swm_exposure_dict['qty']

        campaign_equity = pd.DataFrame(campaign_dict).ffill().sum(axis=1)
        campaign_deltas = pd.DataFrame(campaign_deltas_dict).sum(axis=1)
        campaign_costs = pd.DataFrame(campaign_costs_dict).sum(axis=1)

        campaign_stats = pd.DataFrame({'Change': campaign_equity.diff(), 'Delta': campaign_deltas, 'Costs': campaign_costs})

        print(campaign_stats.tail())

    def report_all(self):
        self.report_pnl()
        self.report_exo_exposure()
        self.report_alpha_exposure()
        self.report_positions()

if __name__ == '__main__':
    from scripts.settings import *
    # from backtester.reports.campaign_report import CampaignReport
    from exobuilder.data.assetindex_mongo import AssetIndexMongo
    from exobuilder.data.datasource_sql import DataSourceSQL
    from exobuilder.data.exostorage import EXOStorage

    assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)
    storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
    datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, assetindex, 3, 20, storage)

    rpt = CampaignReport('ES_Bidirectional V3', datasource)
    rpt.report_all()