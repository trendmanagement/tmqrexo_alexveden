import unittest

from tradingcore.swarmonlinemanager import SwarmOnlineManager
import pandas as pd

class SwarmOnlineManagerTestCase(unittest.TestCase):
    def test_alpha_params(self):
        params = {
            'alpha_params': [
            {
                "opt_params": "(-1, 20, 10, 14)"
            },
            {
                "opt_params": "(-1, 50, 5, 22)"
            }
            ]
        }

        expected = [(-1, 20, 10, 14), (-1, 50, 5, 22)]

        self.assertEqual(expected, SwarmOnlineManager.get_alpha_params(params))

    def test_alpha_positions(self):
        inpos_df = pd.read_csv('inposition_df.csv', index_col=0)

        print(inpos_df)

        expected = [
            {
                "opt_params": "(-1, 10, 15, 18)",
                'position': -1,
            },
            {
                "opt_params": "(1, 10, 15, 2)",
                'position': 1,
            },
            {
                "opt_params": "(1, 10, 15, 22)",
                'position': 0,
            }
        ]

        self.assertEqual(expected, SwarmOnlineManager.get_alpha_positions(inpos_df))


if __name__ == '__main__':
    unittest.main()
