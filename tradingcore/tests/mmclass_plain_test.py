import unittest
from tradingcore.moneymanagement import PlainMM

class PlainMMTestCase(unittest.TestCase):
    def test_init(self):
        acc_info = {
            'size_factor': 1.0,
        }
        mmclass = PlainMM(acc_info)

        self.assertEqual(1.0, mmclass.size_factor)

    def test_init_missed_options(self):
        acc_info = {
        }
        self.assertRaises(ValueError, PlainMM, acc_info)

    def test_init_wrong_size_factor_value(self):
        acc_info = {
            'size_factor': 0.0,
        }
        self.assertRaises(ValueError, PlainMM, acc_info)

        acc_info = {
            'size_factor': -1.0,
        }
        self.assertRaises(ValueError, PlainMM, acc_info)

    def test_get_positions(self):
        campaign_pos = {
            'asset1': {
                'asset': {
                    'name': 'asset1',
                    '_type': 'opt',
                },
                'qty': 1.0,
                'prev_qty': 0.0
            },
            'asset2': {
                'asset': {
                    'name': 'asset1',
                    '_type': 'opt',
                },
                'qty': 0.0,
                'prev_qty': 2.0
            }
        }
        acc_info = {
            'size_factor': 2.0,
        }
        mmclass = PlainMM(acc_info)

        self.assertEqual(mmclass.get_positions(campaign_pos)['asset1']['qty'], 2)
        self.assertEqual(mmclass.get_positions(campaign_pos)['asset1']['prev_qty'], 0.0)

        self.assertEqual(mmclass.get_positions(campaign_pos)['asset2']['qty'], 0)
        self.assertEqual(mmclass.get_positions(campaign_pos)['asset2']['prev_qty'], 4.0)

    def test_get_positions_rounded(self):
        campaign_pos = {
            'asset1': {
                'asset': {
                    'name': 'asset1',
                    '_type': 'opt',
                },
                'qty': 1.0,
                'prev_qty': 3.0
            },
            'asset2': {
                'asset': {
                    'name': 'asset1',
                    '_type': 'opt',
                },
                'qty': 0.0,
                'prev_qty': 2.0
            }
        }
        acc_info = {
            'size_factor': 2.25,
        }
        mmclass = PlainMM(acc_info)

        self.assertEqual(mmclass.get_positions(campaign_pos)['asset1']['qty'], 2)
        self.assertEqual(mmclass.get_positions(campaign_pos)['asset1']['prev_qty'], 7.0)

        self.assertEqual(mmclass.get_positions(campaign_pos)['asset2']['qty'], 0)
        self.assertEqual(mmclass.get_positions(campaign_pos)['asset2']['prev_qty'], 4.0)




if __name__ == '__main__':
    unittest.main()

