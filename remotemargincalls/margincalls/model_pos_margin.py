from scripts.settings import *
from pymongo import MongoClient

from remotemargincalls.margincalls import cmemargincalls
from remotemargincalls.margincalls import cmecore_xmlgeneration

class ModelPosCoreMargin:

    def __init__(self):
        self.mongoclient = MongoClient(MONGO_CONNSTR)
        self.db = self.mongoclient[MONGO_EXO_DB]

        self.fill_instruments()

    def fill_instruments(self):

        instruments = self.db.instruments.find()
        self.instrument_dict = {}
        for instrument in instruments:
            self.instrument_dict[instrument['idinstrument']] = instrument

        exchanges = self.db.exchange.find()
        self.exchanges_dict = {}
        for exchange in exchanges:
            self.exchanges_dict[exchange['idexchange']] = exchange


    def get_cme_core_margin(self, pos_last):

        portfolioLine = cmecore_xmlgeneration.fill_data_line_header_object()

        for contract, exp_dict in pos_last.items():

            # print(exp_dict['optionyear'])

            if exp_dict['qty'] != 0:
                print(contract, exp_dict['qty'])
                # print(exp_dict)
                asset = exp_dict['asset']

                # portfolioLine += cmecore_xmlgeneration.fill_data_line_object \
                #    ('acct1', 'NYMEX', 'CALL', 'CL', 'LO', 2017, 5, 2017, 5, 50, 3)
                instrument_info = self.instrument_dict[asset['idinstrument']]

                # print(instrument_info)

                if asset['optioncode'].strip() == '':
                    option_code = instrument_info['spanoptioncode']
                else:
                    option_code = asset['optioncode']
                # option_code = instrument_info['spanoptioncode']
                # print(option_code)

                if asset['callorput'] == 'C':
                    product_code = 'CALL'
                elif asset['callorput'] == 'P':
                    product_code = 'PUT'
                else:
                    product_code = 'FUTURE'

                future_contract = self.db.contracts.find_one({'idcontract': asset['idcontract']})
                # print(instrument_info['idexchange'])
                # print(exchanges_dict[instrument_info['idexchange']])
                # print(exchanges_dict[instrument_info['idexchange']]['spanexchwebapisymbol'])

                strike_price = cmecore_xmlgeneration.format_strike_for_cme_core(asset['idinstrument'], asset['strikeprice'])

                portfolioLine += cmecore_xmlgeneration.fill_data_line_object \
                    ('acct1', self.exchanges_dict[instrument_info['idexchange']]['spanexchwebapisymbol'], \
                     product_code, instrument_info['spanfuturecode'], \
                     option_code, future_contract['year'], future_contract['monthint'], asset['optionyear'], \
                     asset['optionmonthint'], strike_price, int(exp_dict['qty']))

        xml_file = cmecore_xmlgeneration.create_xml(portfolioLine)

        return cmemargincalls.main_make_margin_call_cme_core(xml_file)

        #margin = cmemargincalls.main_make_margin_call_cme_core(xml_file)

        # print(margin['status'])
        # print(margin['init'])
        # print(margin['maint'])

        #print(margin)