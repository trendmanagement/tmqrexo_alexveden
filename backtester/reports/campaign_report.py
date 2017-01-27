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

        for k, v in self.swarms_data.items():
            seriesdf = v['swarm_series']
            last_date = max(last_date, seriesdf.index[-1])
            prev_date = max(prev_date, seriesdf.index[-2])

        for k, v in self.swarms_data.items():
            instrument = k.split('_')[0]
            seriesdf = v['swarm_series']
            asset_info = self.datasource.assetindex.get_instrument_info(instrument)
            exec_time, decision_time = AssetIndexMongo.get_exec_time(datetime.now(), asset_info)

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

        self.last_date = last_date
        self.prev_date = prev_date

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

        print("\nPnL for current date: {0}".format(pos_last.pnl - pos_prev.pnl))

    def report_all(self):
        self.report_exo_exposure()
        self.report_alpha_exposure()
        self.report_positions()
