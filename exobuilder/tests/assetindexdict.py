from exobuilder.data.assetindex import AssetIndexBase
import pickle
import gzip
import os


class AssetIndexDicts(AssetIndexBase):
    def __init__(self):
        self.instr_name = 'EP'

        proj_path = os.getenv('TMQRPATH', '/home/ubertrader/Dropbox/tmqrexo/tmqrv/')

        os.chdir(os.path.join(proj_path, 'exobuilder', 'tests'))

        with gzip.GzipFile(self.instr_name + '_instrument.pgz', 'r') as f:
            self.instrument_dict = pickle.load(f)

        with gzip.GzipFile(self.instr_name + '_futures.pgz', 'r') as f:
            self.futures_dict = pickle.load(f)

        with gzip.GzipFile(self.instr_name + '_options.pgz', 'r') as f:
            self.options_dict = pickle.load(f)

    def get_instrument_info(self, symbol):
        return self.instrument_dict

    def get_futures_list(self, date, instrument, limit):
        return self.futures_dict

    def get_options_list(self, date, futurecontract):
        return self.options_dict

    def get_instrument(self, dbid):
        if dbid == self.instrument_dict['idinstrument']:
            return self.instrument_dict

    def get_future_contract(self, dbid):
        for d in self.futures_dict:
            if d['idcontract'] == dbid:
                return d

    def get_option_contract(self, dbid):
        for o in self.options_dict[2]['chain']:
            if o['idoption'] == dbid:
                return o


