import unittest
from tradingcore.campaign import Campaign
from bson.objectid import ObjectId
from pymongo import MongoClient
import pandas as pd
from datetime import datetime


class ExoStorageTest1:
    def swarms_data(self, alpha_list=None):
        dt_full = [
            pd.Timestamp("2015-01-01"),
            pd.Timestamp("2015-01-02"),
            pd.Timestamp("2015-01-03"),
            pd.Timestamp("2015-01-04"),
            pd.Timestamp("2015-01-05"),
            pd.Timestamp("2015-01-06"),
            pd.Timestamp("2015-01-07"),
            ]

        dt_not_full = [
            pd.Timestamp("2015-01-01"),
            pd.Timestamp("2015-01-02"),
            pd.Timestamp("2015-01-03"),
            pd.Timestamp("2015-01-04"),
            pd.Timestamp("2015-01-05"),
        ]
        # Full series
        alpha1_exposure = [0, 0, 0, 1, 1, 0, 0]
        alpha2_exposure = [0, 0, 0, 1, 3, 0, 1]

        # not full
        alpha3_exposure = [0, 0, 0, 1, 2]

        return {
            'alpha1': {
                'exo_name': 'exo1',
                'instrument': 'ES',
                'last_exposure': 1.0,
                'swarm_series': pd.DataFrame(
                    {
                        'exposure': alpha1_exposure
                    },
                    index=dt_full
                )
            },
            'alpha2': {
                'exo_name': 'exo1',
                'last_exposure': -2.0,
                'instrument': 'CL',
                'swarm_series': pd.DataFrame(
                    {
                        'exposure': alpha2_exposure
                    },
                    index=dt_full
                )
            },
            'alpha3': {
                'last_exposure': -2.0,
                'exo_name': 'exo2',
                'instrument': 'ES',
                'swarm_series': pd.DataFrame(
                    {
                        'exposure': alpha3_exposure
                    },
                    index=dt_not_full
                ),

            },
        }




    def swarms_positions(self, alpha_list=None):
        return {
            'alpha1': {
                'exposure': 1.0,
                'prev_exposure': 0.0,
                'exo_name': 'exo1'
            },
            'alpha2': {
                'exposure': -2.0,
                'prev_exposure': 2.0,
                'exo_name': 'exo1'
            },
            'alpha3': {
                'exposure': -2.0,
                'prev_exposure': -2.0,
                'exo_name': 'exo2'
            }
        }
    def load_exo(self, exo_name):
        if exo_name == 'exo1':
            return {
                'position': { 'positions': {
                    1:
                         {
                             'asset': 'assetinfo',
                             'qty': 20,
                         },
                    3: {
                             'asset': 'assetinfo',
                             'qty': -20,
                         },
                    },
                }}

        if exo_name == 'exo2':
            return {
                'position': { 'positions': {
                    2:
                         {
                             'asset': 'assetinfo',
                             'qty': 20,
                         },
                    3: {
                             'asset': 'assetinfo',
                             'qty': 20,
                         },
                    },
                }
            }

        raise NotImplementedError('weird')


class DataSourceTest1:
    def __init__(self):
        self.exostorage = ExoStorageTest1()
    def get_info(self, hash):
        if hash == 1:
            return {'name': 'FUT1', 'info': 'test'}
        if hash == 2:
            return {'name': 'FUT2', 'info': 'test'}
        if hash == 3:
            return {'name': 'OPT1', 'info': 'test'}


class CampaignTestCase(unittest.TestCase):
    def setUp(self):
        self._dict = {
            'name': 'test_campaign',
            'description': 'Brief description of campaign',
            '_id': ObjectId("57b42aba82d9c39e0341fbc7"),
            'alphas': {
                'alpha1': {
                    'qty': -1.0,
                    'leg_name': 'leg1',
                },
                'alpha2': {
                    'qty': -2.0,
                },
                'alpha3': {
                    'qty': 2.0,
                    'leg_name': 'leg2',
                },
            }
        }

        client = MongoClient('mongodb://localhost:27017/')
        self._db = client['tmqr']
        self._datasource = DataSourceTest1()

        self._cmp = Campaign(self._dict, self._datasource)


    def test_campaign_init(self):
        cmp = Campaign(self._dict, self._datasource)
        self.assertEqual(self._dict, cmp._dict)

        self.assertEqual(['', 'leg1', 'leg2'], self._cmp.legs)

    def test_campaign_has_name(self):
        self.assertEqual('test_campaign', self._cmp.name)

    def test_campaign_has_description(self):
        self.assertEqual('Brief description of campaign', self._cmp.description)

    def test_campaign_has_dbid(self):
        self.assertEqual(ObjectId("57b42aba82d9c39e0341fbc7"), self._cmp.dbid)

    def test_campaign_has_alphas(self):
        self.assertEqual(self._dict['alphas'], self._cmp.alphas)

        # Create empty dict is 'alphas' don't exist
        del self._dict['alphas']
        self.assertEqual({}, self._cmp.alphas)

    def test_campaign_alpha_position(self):
        pos = self._cmp.alphas_positions(None)

        self.assertEqual(3, len(pos))
        self.assertEqual(-1.0, pos['alpha1']['exposure'])
        self.assertEqual('exo1', pos['alpha1']['exo_name'])

        self.assertEqual(4.0, pos['alpha2']['exposure'])
        self.assertEqual('exo1', pos['alpha2']['exo_name'])

        self.assertEqual(-4.0, pos['alpha3']['exposure'])
        self.assertEqual('exo2', pos['alpha3']['exo_name'])

    def test_campaign_alpha_is_active_now(self):
        _dict = {
            'name': 'test_campaign',
            'description': 'Brief description of campaign',
            '_id': ObjectId("57b42aba82d9c39e0341fbc7"),
            'alphas': {
                'alpha1': {
                    'qty': -1.0,
                    'leg_name': 'leg1',
                    'end': datetime(2016, 1, 1),
                    'begin': datetime(2011, 1, 1)
                },
                'alpha2': {
                    'qty': -2.0,
                    'end': datetime(2011, 1, 1),
                },
                'alpha3': {
                    'qty': 2.0,
                    'leg_name': 'leg2',
                    'begin': datetime(2016, 1, 1),
                },
            }
        }

        _cmp = Campaign(_dict, self._datasource)
        self.assertEqual(True, _cmp.alpha_is_active('alpha1', datetime(2015, 1, 1)))
        self.assertEqual(False, _cmp.alpha_is_active('alpha1', datetime(2016, 1, 1)))
        self.assertEqual(True, _cmp.alpha_is_active('alpha1', datetime(2011, 1, 1)))
        self.assertEqual(False, _cmp.alpha_is_active('alpha1', datetime(2016, 1, 2)))
        self.assertEqual(False, _cmp.alpha_is_active('alpha1', datetime(2010, 12, 31)))

        self.assertEqual(False, _cmp.alpha_is_active('alpha2', datetime(2015, 1, 1)))
        self.assertEqual(False, _cmp.alpha_is_active('alpha2', datetime(2016, 1, 1)))
        self.assertEqual(False, _cmp.alpha_is_active('alpha2', datetime(2011, 1, 2)))
        self.assertEqual(False, _cmp.alpha_is_active('alpha2', datetime(2011, 1, 1)))
        self.assertEqual(True, _cmp.alpha_is_active('alpha2', datetime(2010, 12, 31)))

        self.assertEqual(True, _cmp.alpha_is_active('alpha3', datetime(2025, 1, 1)))
        self.assertEqual(True, _cmp.alpha_is_active('alpha3', datetime(2016, 1, 1)))
        self.assertEqual(False, _cmp.alpha_is_active('alpha3', datetime(2011, 1, 2)))
        self.assertEqual(False, _cmp.alpha_is_active('alpha3', datetime(2015, 12, 31)))




    def test_campaign_exo_positions(self):
        pos = self._cmp.exo_positions(None)

        self.assertEqual(2, len(pos))
        self.assertEqual(3.0, pos['exo1']['exposure'])
        self.assertEqual(-4.0, pos['exo2']['exposure'])

    def test_campaign_net_positions(self):
        pos = self._cmp.positions

        self.assertEqual(3, len(pos))
        self.assertEqual(20 * 3, pos['FUT1']['qty'])
        self.assertEqual(20 * -4, pos['FUT2']['qty'])
        self.assertEqual(-20*3 + 20*-4, pos['OPT1']['qty'])

    def test_campaign_add(self):
        alpha_name = 'new_alpha'
        alpha_leg = 'leg1'
        campaign_qty = 2.0
        self._cmp.alphas_add(alpha_name, campaign_qty, alpha_leg)
        self.assertEqual(sorted(['alpha1', 'alpha2', 'alpha3', 'new_alpha']), sorted(list(self._cmp.alphas.keys())))

    def test_campaign_has_legs(self):
        alpha_name = 'new_alpha'
        alpha_leg = 'leg1'
        campaign_qty = 2.0
        # Clean alpha list
        self._cmp._dict['alphas'] = {}
        self._cmp._legs = {}
        self._cmp.alphas_add(alpha_name, campaign_qty, alpha_leg)
        self.assertEqual(True, 'leg1' in self._cmp._legs)
        self.assertEqual(['leg1'], self._cmp.legs)

    def test_campaign_has_alpha_list(self):
        campaign_qty = 2.0
        self._cmp.alphas_add("new_alpha1", campaign_qty, 'leg1')
        self._cmp.alphas_add("new_alpha2", campaign_qty, 'leg2')
        self._cmp.alphas_add("new_alpha3", campaign_qty)
        self.assertEqual(['', 'leg1', 'leg2'], self._cmp.legs)

        self.assertEqual(['alpha1', 'alpha2', 'alpha3', 'new_alpha1', 'new_alpha2', 'new_alpha3'], self._cmp.alphas_list())

        self.assertEqual(['alpha1', 'new_alpha1'], self._cmp.alphas_list(by_leg='leg1'))
        self.assertEqual(['alpha3', 'new_alpha2'], self._cmp.alphas_list(by_leg='leg2'))
        self.assertEqual(['alpha2', 'new_alpha3'], self._cmp.alphas_list(by_leg=''))
        self.assertEqual(['alpha2', 'new_alpha3'], self._cmp.alphas_list(by_leg=None))

    def test_swarms_positions_on_date(self):
        """
        dt_full = [
            pd.Timestamp("2015-01-01"),
            pd.Timestamp("2015-01-02"),
            pd.Timestamp("2015-01-03"),
            pd.Timestamp("2015-01-04"),
            pd.Timestamp("2015-01-05"),
            pd.Timestamp("2015-01-06"),
            pd.Timestamp("2015-01-07"),
            ]

        dt_not_full = [
            pd.Timestamp("2015-01-01"),
            pd.Timestamp("2015-01-02"),
            pd.Timestamp("2015-01-03"),
            pd.Timestamp("2015-01-04"),
            pd.Timestamp("2015-01-05"),
        ]

        # alpha1_exposure = [0, 0, 0, 1, 1, 0, 0]
        alpha2_exposure   = [0, 0, 0, 1, 3, 0, 1]
        # not full
        alpha3_exposure =   [0, 0, 0, 1, 2]

        'alphas': {
                'alpha1': {
                    'qty': -1.0,
                    'leg_name': 'leg1',
                },
                'alpha2': {
                    'qty': -2.0,
                },
                'alpha3': {
                    'qty': 2.0,
                    'leg_name': 'leg2',
                },
            }
        """
        p = self._cmp.alphas_positions(datetime(2015, 1, 1))
        self.assertEqual(0, p['alpha1']['exposure'])
        self.assertEqual(0, p['alpha2']['exposure'])
        self.assertEqual(0, p['alpha3']['exposure'])

        p = self._cmp.alphas_positions(datetime(2015, 1, 4))
        self.assertEqual(-1, p['alpha1']['exposure'])
        self.assertEqual(-2, p['alpha2']['exposure'])
        self.assertEqual(2, p['alpha3']['exposure'])

        p = self._cmp.alphas_positions(datetime(2015, 1, 5))
        self.assertEqual(-1, p['alpha1']['exposure'])
        self.assertEqual(-6, p['alpha2']['exposure'])
        self.assertEqual(4, p['alpha3']['exposure'])

        p = self._cmp.alphas_positions(datetime(2015, 1, 6))
        self.assertEqual(0, p['alpha1']['exposure'])
        self.assertEqual(0, p['alpha2']['exposure'])
        self.assertEqual(4, p['alpha3']['exposure'])

        p = self._cmp.alphas_positions(datetime(2015, 1, 7))
        self.assertEqual(0, p['alpha1']['exposure'])
        self.assertEqual(-2, p['alpha2']['exposure'])
        self.assertEqual(4, p['alpha3']['exposure'])

    def test_exo_positions_on_date(self):
        """
        dt_full = [
            pd.Timestamp("2015-01-01"),
            pd.Timestamp("2015-01-02"),
            pd.Timestamp("2015-01-03"),
            pd.Timestamp("2015-01-04"),
            pd.Timestamp("2015-01-05"),
            pd.Timestamp("2015-01-06"),
            pd.Timestamp("2015-01-07"),
            ]

        dt_not_full = [
            pd.Timestamp("2015-01-01"),
            pd.Timestamp("2015-01-02"),
            pd.Timestamp("2015-01-03"),
            pd.Timestamp("2015-01-04"),
            pd.Timestamp("2015-01-05"),
        ]

        # alpha1_exposure = [0, 0, 0, 1, 1, 0, 0]
        alpha2_exposure   = [0, 0, 0, 1, 3, 0, 1]
        # not full
        alpha3_exposure =   [0, 0, 0, 1, 2]

        'alphas': {
                'alpha1': {
                exo1
                    'qty': -1.0,
                    'leg_name': 'leg1',
                },
                'alpha2': {
                exo1
                    'qty': -2.0,
                },
                'alpha3': {
                exo2
                    'qty': 2.0,
                    'leg_name': 'leg2',
                },
            }
        """

        p = self._cmp.exo_positions(datetime(2015, 1, 5))
        self.assertEqual(-7, p['exo1']['exposure'])
        self.assertEqual(4, p['exo2']['exposure'])

        p = self._cmp.exo_positions(datetime(2015, 1, 7))
        self.assertEqual(-2, p['exo1']['exposure'])
        self.assertEqual(4, p['exo2']['exposure'])



if __name__ == '__main__':
    unittest.main()
