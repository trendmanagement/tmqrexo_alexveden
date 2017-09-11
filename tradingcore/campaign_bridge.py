"""
This is a bridging module for a new TMQR Framework 2.0

This module help to use previously calculated alphas and theirs positions

"""
from pymongo import MongoClient
import pandas as pd
import pickle
import lz4
import re
from datetime import datetime
import warnings
from exobuilder.contracts.futurecontract import FUT_HASH_ROOT
from exobuilder.contracts.optioncontract import OPT_HASH_ROOT


COLLECTION_ASSET_INFO = 'asset_info'
COLLECTION_ASSET_INDEX = 'asset_index'
COLLECTION_ALPHA_DATA = 'alpha_data'

ALPHA_NEW_PREFIX = "!NEW_"

MONGO_CONNSTR = 'mongodb://tmqr:tmqr@10.0.1.2/tmqr2?authMechanism=SCRAM-SHA-1'
#MONGO_CONNSTR = 'mongodb://localhost/'
MONGO_DB = 'tmqr2'


class CampaignBridge:
    def __init__(self, **kwargs):
        mongo_host = kwargs.get('host', MONGO_CONNSTR)
        mongo_db = kwargs.get('db', MONGO_DB)

        self.client = MongoClient(mongo_host)
        self.db = self.client[mongo_db]

        self._instrument_info_cache = {}

    def object_load_decompress(self, obj):
        """
        Decompress and unpickle object from byte data and create object instance
        :param obj:
        :return:
        """
        return pickle.loads(lz4.block.decompress(obj))

    def swarms_list(self, instruments_list=('*',), alpha_list=('*',)):
        """
        Select swarms from Mongo using case INSENSITIVE filters (wildcards allowed)
        :param instruments_list: instruments list filter like '*', 'CL*', 'CL*9'
        :param direction: direction filter (1=Long, -1=Short, 0=Bidirectional)
        :param alpha_list: alpha name filter
        :param exo_list: exo list filter
        :return: Pandas.DataFrame(swarms_picked_equity), list(mongo_swarms_dicts)
        """
        def re_pattern(values_list, prepend='', append=''):
            result = ""
            for i,v in enumerate(values_list):
                re_val = v.replace('*', '.*').replace(ALPHA_NEW_PREFIX, '')

                if i == 0:
                    result += '{0}({1}'.format(prepend, re_val)
                else:
                    result += '|{0}'.format(re_val)

            result += '){0}'.format(append)

            return re.compile(result, re.IGNORECASE)

        cursor = self.db[COLLECTION_ALPHA_DATA].find(
            {'$and':
                [
                    {'name': re_pattern(instruments_list, prepend='^')},
                    {'name': re_pattern(alpha_list)}
                ]
            }
        )

        swarm_data = []

        for _swm_data in cursor:
            _alpha_data = self.db_load_alpha(ALPHA_NEW_PREFIX+_swm_data['name'], alpha_data=_swm_data)
            swarm_data.append(_alpha_data)

        series_dict = {}

        for s in swarm_data:
            series_dict[s['swarm_name']] = s['swarm_series']['equity']

        return series_dict, swarm_data

    def db_load_alpha(self, alpha_name, alpha_data=None):
        """
        Loads index data from the MongoDB
        :param alpha_name: name of new alpha (can contain '!NEW_' prefix)
        :param alpha_data: pre-loaded MongoDB record for alpha data
        :return:
        """
        if alpha_data is None:
            alpha_data = self.db[COLLECTION_ALPHA_DATA].find_one({'name': alpha_name.replace(ALPHA_NEW_PREFIX, "")})
            if alpha_data is None:
                raise KeyError("Alpha {0} is not found in the DB".format(alpha_name))

        alpha_dict = {
            'name': alpha_name,
            'swarm_name': alpha_name,
            'swarm_series': self.object_load_decompress(alpha_data['stats']).get('series', pd.DataFrame()),
            'position': self.object_load_decompress(alpha_data['position']['data']),
            'instrument': 'N/A'
        }

        alpha_dict['swarm_series'].index = alpha_dict['swarm_series'].index.map(lambda d: datetime(d.year, d.month, d.day))
        if 'delta' not in alpha_dict['swarm_series'].columns:
            alpha_dict['swarm_series']['delta'] = float('nan')

        return alpha_dict

    def db_get_instrument_info(self, instrument):
        """
        Fetch asset info
        :param instrument:
        :return: asset info Mongo dict
        """
        # checking cache
        ainfo_default = self._instrument_info_cache.get(instrument, None)
        if ainfo_default:
            return ainfo_default


        toks = instrument.split('.')
        if len(toks) != 2:
            raise ValueError("Instrument name must be <MARKET>.<INSTRUMENT>")
        mkt_name, instr_name = toks

        ainfo_default = self.db[COLLECTION_ASSET_INFO].find_one({'instrument': '{0}.$DEFAULT$'.format(mkt_name)})
        if ainfo_default is None:
            raise KeyError(
                "{0}.$DEFAULT$ record is not found in 'asset_info' collection".format(mkt_name))

        ainfo_instrument = self.db[COLLECTION_ASSET_INFO].find_one({'instrument': '{0}'.format(instrument)})

        if ainfo_instrument is not None:
            ainfo_default.update(ainfo_instrument)
        else:
            ainfo_default['instrument'] = instrument

        # Setting cache
        self._instrument_info_cache[instrument] = ainfo_default

        return ainfo_default

    def db_get_contract_info(self, tckr):
        """
        Fetch contract information by full qualified ticker
        :param tckr: full qualified ticker
        :return: Contract info Mongo dict
        """

        result = self.db[COLLECTION_ASSET_INDEX].find_one({'tckr': tckr})
        if result is None:
            raise KeyError("Contract info for {0} not found".format(tckr))

        return result

    @staticmethod
    def alpha_check_is_active_by_dict(sett_dict, date):
        assert date is not None
        date_begin = sett_dict.get('begin', datetime(1900, 1, 1))
        date_end = sett_dict.get('end', datetime(2100, 1, 1))

        assert date_end > date_begin

        return date.date() >= date_begin.date() and date.date() < date_end.date()

    def get_alphas_raw_positions(self, alpha_dict, position_date=None):
        """
        Get new framework alphas from campaign, calculate campaign net position
        :param alpha_dict: campaign.alphas - dictionary of <alpha_name, dict<alpha_param, value>>
        :param position_date: date of position aggregation
        :return:
        """
        new_alphas_positions = {}

        target_date = datetime.now() if position_date is None else position_date

        for alpha_name, alpha_params in alpha_dict.items():
            if not alpha_name.startswith(ALPHA_NEW_PREFIX):
                # Skip old framework alphas
                continue

            if not self.alpha_check_is_active_by_dict(alpha_params, target_date):
                # Skip not engaged alphas
                continue


            alpha_rec = self.db_load_alpha(alpha_name)

            try:
                dt, pos = alpha_rec['position'].popitem()
                while dt.date() > target_date.date():
                    # Or Raises KeyError
                    dt, pos = alpha_rec['position'].popitem()

                # Apply alpha qty
                alpha_pos = {}
                for ticker, pos_rec in pos.items():
                    alpha_pos[ticker] = (pos_rec[0], pos_rec[1], pos_rec[2]*alpha_params['qty'])

                new_alphas_positions[alpha_name] = {
                    'dt': dt.date(),
                    'pos': alpha_pos,
                }

            except KeyError:
                continue

        return new_alphas_positions

    def merge_alphas_positions(self, new_alphas_positions):
        net_position = {}

        max_dt = None
        for alpha_name, pos_dict in new_alphas_positions.items():
            if max_dt is None:
                max_dt = pos_dict['dt']
            else:
                max_dt = max(max_dt, pos_dict['dt'])

        for alpha_name, pos_dict in new_alphas_positions.items():

            if pos_dict['dt'] < max_dt:
                # Check for delayed alphas
                warnings.warn('New 2.0 alphas position is delayed: {0}, '
                              'alpha position date: {1}, last date: {2} '.format(alpha_name, pos_dict['dt'], max_dt))

            for ticker, pos_rec in pos_dict['pos'].items():
                old_qty = net_position.setdefault(ticker, (0.0, 0.0))
                new_qty = old_qty[1] + pos_rec[2]
                if new_qty == 0:
                    del net_position[ticker]
                else:
                    net_position[ticker] = (pos_rec[0], new_qty) # 2.0 Position's: (decision_price, qty) tuple

        return net_position




    def convert_position(self, net_position):
        converted_position = {}
        for new_ticker, pos_rec in net_position.items():
            result = self.db_get_contract_info(new_ticker)

            dbid = result['extra_data']['sqlid']
            ctype = result['type']
            instrument = result['instr']

            iinfo = self.db_get_instrument_info(instrument)

            if ctype == 'F':
                contract_hash = dbid + FUT_HASH_ROOT
                point_value = 1.0 / iinfo['ticksize'] * iinfo['tickvalue']
            else:
                contract_hash = dbid + OPT_HASH_ROOT
                point_value = 1.0 / iinfo['ticksize_options'] * iinfo['tickvalue_options']

            converted_position[contract_hash] = {
                'leg_name': '',
                'qty': pos_rec[1],
                'value':  pos_rec[0] * point_value * pos_rec[1],
            }
        return {
            '_realized_pnl': 0.0,
            '_last_trans_date': datetime.now(),
            'positions': converted_position
        }

    def _calc_transactions(self,
                           date: datetime,
                           current_pos,
                           prev_pos):
        """
        Calculate transactions based on current and previous positions records
        :param date:
        :param current_pos: current position record
        :param prev_pos: previous position record
        :return: transaction dictionary record
        """
        result = {}

        assert current_pos is not None, 'current_pos must be initialized'
        iDPX = 0
        iEPX = 1
        iQTY = 2

        if prev_pos is None:
            intersected_assets = set(current_pos)
        else:
            intersected_assets = set(current_pos) | set(prev_pos)

        for asset in intersected_assets:
            prev_values = prev_pos.get(asset, None) if prev_pos is not None else None
            curr_values = current_pos.get(asset, None)

            if prev_values is None:
                result[asset] = (curr_values[iDPX], curr_values[iEPX], curr_values[iQTY])
            elif curr_values is None:
                # Skip old closed positions
                if prev_values[iQTY] != 0:
                    warnings.warn("Can't get actual prices for position from positions data, using prev day price: "
                                  "Asset: {0} Date: {1}".format(asset, date))
                    result[asset] = (prev_values[iDPX], prev_values[iEPX], -prev_values[iQTY])
            else:
                # Calculating transactions for existing position
                trans_qty = curr_values[iQTY] - prev_values[iQTY]
                if trans_qty != 0:
                    result[asset] = (curr_values[iDPX], curr_values[iEPX], trans_qty)

        return result


    def get_alphas_transactions_list(self, alpha_dict, position_date=None):
        """
        Get list of transactions made by alphas of the campaign
        :param alpha_dict: campaign.alphas - dictionary of <alpha_name, dict<alpha_param, value>>
        :param position_date: date of position aggregation
        :return:
        """
        transactions_list = []

        target_date = datetime.now() if position_date is None else position_date

        for alpha_name, alpha_params in alpha_dict.items():
            if not alpha_name.startswith(ALPHA_NEW_PREFIX):
                # Skip old framework alphas
                continue

            if not self.alpha_check_is_active_by_dict(alpha_params, target_date):
                # Skip not engaged alphas
                continue


            alpha_rec = self.db_load_alpha(alpha_name)

            prev_pos = None
            for dt, pos in alpha_rec['position'].items():
                if dt.date() > target_date.date():
                    break

                _trans = self._calc_transactions(dt, pos, prev_pos)

                for ticker, pos_rec in _trans.items():
                    """
                    Transaction dict format
                    {
                        "price" : 8.73745113870518,
                        "date" : ISODate("2011-06-01T12:45:00.000Z"),
                        "qty" : 1.0,
                        "usdvalue" : 436.872556935259,
                        "asset" : {
                            "dbid" : 14975,
                            "hash" : 200014975,
                            "type" : "O",
                            "name" : "P.US.EPM1112900"
                        }
                    }
                    """
                    transactions_list.append({
                        'tckr': ticker,       # Temporary field
                        'price': pos_rec[0],  # Use decision price
                        'date': dt.replace(tzinfo=None),          # Store datetime, but not TZ-aware!
                        'qty': pos_rec[2] * alpha_params['qty'],  # Don't forget take into account alpha qty
                        'usdvalue': 0.0,                          # We will update this field later
                        # 'asset' : { } <- add this field later
                    })

                prev_pos = pos

        #
        # Update instrument info and usd values
        #

        # Get unique set of new framework's tickers and their contract info
        contract_info = {}
        for ticker in set([t['tckr'] for t in transactions_list]):
            contract_info[ticker] = self.db_get_contract_info(ticker)

        # Update asset information and
        for trans in transactions_list:

            ticker = trans['tckr']
            # delete temporary field
            del trans['tckr']

            dbid = contract_info[ticker]['extra_data']['sqlid']
            ctype = contract_info[ticker]['type']
            instrument = contract_info[ticker]['instr']
            iinfo = self.db_get_instrument_info(instrument)

            if ctype == 'F':
                contract_hash = dbid + FUT_HASH_ROOT
                point_value = 1.0 / iinfo['ticksize'] * iinfo['tickvalue']
                asset_type = 'F'
            else:
                contract_hash = dbid + OPT_HASH_ROOT
                asset_type = 'O'
                point_value = 1.0 / iinfo['ticksize_options'] * iinfo['tickvalue_options']

            trans['usdvalue'] = trans['price'] * trans['qty'] * point_value
            """
            "asset" : {
                            "dbid" : 14975,
                            "hash" : 200014975,
                            "type" : "O",
                            "name" : "P.US.EPM1112900"
                        }
            """
            # Making compatible asset record for transaction
            trans['asset'] = {
                'dbid': dbid,
                'hash': contract_hash,
                'type': asset_type,
                'name': ticker,  # Using new asset name, this field is unused, contract_hash is used for asset fetching
            }

        return transactions_list


    def get_net_position(self, alphas_dict, date=None):
        """
        Returns position record eligible for online position merging
        :param alphas_dict:
        :param date:
        :return: position dict similar to Position.as_dict() serialization
        """
        raw_pos = self.get_alphas_raw_positions(alphas_dict, date)
        merged_position = self.merge_alphas_positions(raw_pos)

        return self.convert_position(merged_position)






