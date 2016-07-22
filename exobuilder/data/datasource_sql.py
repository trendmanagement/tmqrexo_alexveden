from .datasource import DataSourceBase
from datetime import datetime
import pymssql


class DataSourceSQL(DataSourceBase):
    def __init__(self, server, user, password, assetindex, futures_limit, options_limit, exostorage=None):
        super().__init__(assetindex, futures_limit, options_limit, exostorage=exostorage)
        self. conn = pymssql.connect(server, user + "@" + server, password, "TMLDB")

        # Extradata cache
        self.extra_data_cache = {}


    def get_fut_data(self, dbid, date):
        c2 = self.conn.cursor(as_dict=True)
        c2.execute("SELECT TOP(1) * FROM cqgdb.tblbardata where idcontract = {0} AND datetime <= '{1}' ORDER BY datetime DESC".format(
                dbid, date.isoformat()))

        if c2.rowcount == 0:
            raise KeyError('Futures data not found contract id: {0} date: {1}'.format(dbid, date))

        for row in c2:
            return row


    def get_extra_data(self, key, date):


        if key == 'riskfreerate':
            if key in self.extra_data_cache:
                if date in self.extra_data_cache[key]:
                    return self.extra_data_cache[key][date]

            rfr_dic = self.extra_data_cache.setdefault(key, {})
            #
            #  Getting risk-free-rate on previous day
            #
            c2 = self.conn.cursor(as_dict=True)
            c2.execute(
                "SELECT TOP(1) * FROM cqgdb.tbloptioninputdata where idoptioninputsymbol = 15 AND optioninputdatetime < '{0}' ORDER BY optioninputdatetime DESC".format(
                    date.date().isoformat()))

            for row in c2:
                rfr_result = row


            rfr_dic[date] = rfr_result["optioninputclose"]
            return self.extra_data_cache[key][date]
        else:
            raise KeyError("Unknown key for extra_data, only 'riskfreerate' supported.")

    def get_option_data(self, dbid, date):
        c2 = self.conn.cursor(as_dict=True)
        c2.execute("SELECT TOP(1) * FROM cqgdb.tbloptiondata where idoption = {0} AND datetime < '{1}' ORDER BY datetime DESC".format(
                dbid, date.date().isoformat()))

        if c2.rowcount == 0:
            raise KeyError('Option data not found contract id: {0} date: {1}'.format(dbid, date))

        for row in c2:
            return row


