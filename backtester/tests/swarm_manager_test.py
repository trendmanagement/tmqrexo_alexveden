import unittest
from backtester.swarms.manager import SwarmManager
import pandas as pd
import numpy as np

class SwarmManagerTestCase(unittest.TestCase):
    def test_best_ranking_dtype_is_int8(self):
        sm = SwarmManager()

        index = ['0', '1', '2', '3', '4', '5']
        ranks = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

        rnk = pd.Series(ranks, index=index)

        r = sm._get_nbest(rnk, nsystems=2)
        self.assertEqual(r.dtype, np.int8)

    def test_best_ranking(self):

        sm = SwarmManager()

        index = ['0', '1', '2', '3', '4', '5']
        ranks = [0, 1, 5, 3, 1, 1]

        rnk = pd.Series(ranks, index=index)

        r = sm._get_nbest(rnk, nsystems=2)

        # Indexes is a string, because these are pd.Series indexes not array int32 index
        self.assertEqual(r['0'], 0)
        self.assertEqual(r['1'], 0)
        self.assertEqual(r['2'], 1)
        self.assertEqual(r['3'], 1)
        self.assertEqual(r['4'], 0)
        self.assertEqual(r['5'], 0)


    def test_best_ranking_full_nans(self):
        sm = SwarmManager()

        index = ['0', '1', '2', '3', '4', '5']
        ranks = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

        rnk = pd.Series(ranks, index=index)

        r = sm._get_nbest(rnk, nsystems=2)

        # Indexes is a string, because these are pd.Series indexes not array int32 index
        self.assertEqual(r['0'], 0)
        self.assertEqual(r['1'], 0)
        self.assertEqual(r['2'], 0)
        self.assertEqual(r['3'], 0)
        self.assertEqual(r['4'], 0)
        self.assertEqual(r['5'], 0)


    def test_best_ranking_partial_nans(self):
        sm = SwarmManager()

        index = ['0', '1', '2', '3', '4', '5']
        ranks = [np.nan, 1, 5, np.nan, 9, np.nan]

        rnk = pd.Series(ranks, index=index)

        r = sm._get_nbest(rnk, nsystems=2)

        # Indexes is a string, because these are pd.Series indexes not array int32 index
        self.assertEqual(r['0'], 0)
        self.assertEqual(r['1'], 0)
        self.assertEqual(r['2'], 1)
        self.assertEqual(r['3'], 0)
        self.assertEqual(r['4'], 1)
        self.assertEqual(r['5'], 0)

        self.assertEqual(r.dtype, np.int8)

    def test_best_ranking_negative_and_zeros_filter(self):
        sm = SwarmManager()

        index = ['0', '1', '2', '3', '4', '5']
        ranks = [np.nan, 0, -5, np.nan, 9, np.nan]

        rnk = pd.Series(ranks, index=index)

        r = sm._get_nbest(rnk, nsystems=2)

        # Indexes is a string, because these are pd.Series indexes not array int32 index
        self.assertEqual(r['0'], 0)
        self.assertEqual(r['1'], 0)
        self.assertEqual(r['2'], 0)
        self.assertEqual(r['3'], 0)
        self.assertEqual(r['4'], 1)
        self.assertEqual(r['5'], 0)

        self.assertEqual(r.dtype, np.int8)


if __name__ == '__main__':
    unittest.main()
