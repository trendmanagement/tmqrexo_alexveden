import unittest
import pandas as pd
import numpy as np

from backtester.backtester import backtest, stats

class BacktesterTestCase(unittest.TestCase):
    def test_inposition(self):
        data = {'exo': pd.Series(range(10))}
        entry_rule = pd.Series([0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        exit_rule =  pd.Series([0, 0, 0, 1, 0, 0, 0, 0, 0, 0])

        pl, inpos = backtest(data, entry_rule, exit_rule, direction=1)

        for i in range(len(inpos)):
            # Fix: 2016-05-30 Exit bar is not in position
            exp = pd.Series([0, 1, 1, 0, 0, 0, 0, 0, 0, 0])
            self.assertEqual(exp[i], inpos.values[i])

    def test_pnl(self):
        data = {'exo': pd.Series(range(10))}
        entry_rule = pd.Series([0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        exit_rule =  pd.Series([0, 0, 0, 1, 0, 0, 0, 0, 0, 0])

        pl, inpos = backtest(data, entry_rule, exit_rule, direction=-1)

        for i in range(len(inpos)):
            exp = pd.Series([0, 0, -1, -1, 0, 0, 0, 0, 0, 0])
            self.assertEqual(exp[i], pl.values[i])

    def test_same_bar_exit(self):
        """
        Entering to position even is we have exit_signal on the same bar
        :return:
        """
        data = {'exo': pd.Series(range(10))}
        entry_rule = pd.Series([0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        exit_rule = pd.Series([0, 1, 0, 1, 0, 0, 0, 0, 0, 0])

        pl, inpos = backtest(data, entry_rule, exit_rule, direction=1)

        for i in range(len(inpos)):
            exp = pd.Series([0, 1, 1, 0, 0, 0, 0, 0, 0, 0])
            self.assertEqual(exp[i], inpos.values[i])

        self.assertEqual(True, False, msg="Need to discuss!")

    def test_stats_no_costs(self):
        data = {'exo': pd.Series(range(10))}
        entry_rule = pd.Series([0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        exit_rule = pd.Series([0, 0, 0, 1, 0, 0, 0, 0, 0, 0])

        pl, inpos = backtest(data, entry_rule, exit_rule, direction=1)
        equity, statsistics = stats(pl, inpos, positionsize=pd.Series(1, index=inpos.index), costs=None)

        for i in range(len(equity)):
            exp = pd.Series([0, 0, 1, 2, 2, 2, 2, 2, 2, 2])
            self.assertEqual(exp[i], equity.values[i])

        self.assertEqual(1, statsistics['count'])
        self.assertEqual(2, statsistics['netprofit'])
        self.assertEqual(2, statsistics['avg'])

    def test_stats_no_costs_2trades(self):
        data = {'exo': pd.Series(range(10))}
        entry_rule = pd.Series([0, 1, 0, 0, 0, 1, 0, 0, 0, 0])
        exit_rule =  pd.Series([0, 0, 0, 1, 0, 0, 0, 0, 1, 0])

        pl, inpos = backtest(data, entry_rule, exit_rule, direction=1)
        equity, statsistics = stats(pl, inpos, positionsize=pd.Series(1, index=inpos.index), costs=None)

        for i in range(len(inpos)):
            exp = pd.Series(   [0, 1, 1, 0, 0, 1, 1, 1, 0, 0])
            self.assertEqual(exp[i], inpos.values[i])

        for i in range(len(equity)):
            exp = pd.Series(   [0, 0, 1, 2, 2, 2, 3, 4, 5, 5])
            self.assertEqual(exp[i], equity.values[i])

        self.assertEqual(2, statsistics['count'])
        self.assertEqual(5, statsistics['netprofit'])
        self.assertEqual(2.5, statsistics['avg'])

    def test_stats_no_costs_position_size(self):
        data = {'exo': pd.Series(range(10))}
        entry_rule = pd.Series([0, 1, 0, 0, 0, 1, 0, 0, 0, 0])
        exit_rule =  pd.Series([0, 0, 0, 1, 0, 0, 0, 0, 1, 0])

        pl, inpos = backtest(data, entry_rule, exit_rule, direction=1)
        equity, statsistics = stats(pl, inpos, positionsize=pd.Series(2, index=inpos.index), costs=None)


        for i in range(len(equity)):
            exp = pd.Series([0, 0, 2, 4, 4, 4, 6, 8, 10, 10])
            self.assertEqual(exp[i], equity.values[i])

        self.assertEqual(2, statsistics['count'])
        self.assertEqual(10, statsistics['netprofit'])
        self.assertEqual(5, statsistics['avg'])

    def test_stats_costs(self):
        data = {'exo': pd.Series(range(10))}
        entry_rule = pd.Series([0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        exit_rule =  pd.Series([0, 0, 0, 1, 0, 0, 0, 0, 0, 0])

        pl, inpos = backtest(data, entry_rule, exit_rule, direction=1)
        costs = pd.Series(1, index=inpos.index)

        equity, statsistics = stats(pl, inpos, positionsize=pd.Series(1, index=inpos.index), costs=costs)


        for i in range(len(equity)):
            exp = pd.Series([0, -2, -1, 0, 0, 0, 0, 0, 0, 0])
            self.assertEqual(exp[i], equity.values[i])

        self.assertEqual(1, statsistics['count'])
        self.assertEqual(0, statsistics['netprofit'])
        self.assertEqual(0, statsistics['avg'])

    def test_stats_costs_with_position_size(self):
        data = {'exo': pd.Series(range(10))}
        entry_rule = pd.Series([0, 1, 0, 0, 0, 1, 0, 0, 0, 0])
        exit_rule =  pd.Series([0, 0, 0, 1, 0, 0, 0, 0, 1, 0])

        pl, inpos = backtest(data, entry_rule, exit_rule, direction=1)
        equity, statsistics = stats(pl, inpos, positionsize=pd.Series(2, index=inpos.index), costs=pd.Series(1, index=inpos.index))

        for i in range(len(equity)):
            exp = pd.Series([0, -4, -2, 0, 0, -4, -2, 0, 2, 2])
            self.assertEqual(exp[i], equity.values[i])

        self.assertEqual(2, statsistics['count'])
        self.assertEqual(2, statsistics['netprofit'])
        self.assertEqual(1, statsistics['avg'])

    def test_stats_1bar_inposition(self):
        pl =    pd.Series([0, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        inpos = pd.Series([0, 1, 0, 0, 0, 0, 0, 0, 0, 0])

        equity, statsistics = stats(pl, inpos, positionsize=pd.Series(1, index=inpos.index), costs=pd.Series(1, index=inpos.index))

        for i in range(len(equity)):
            exp = pd.Series([0, -2, -1, -1, -1, -1, -1, -1, -1, -1])
            self.assertEqual(exp[i], equity.values[i])

        self.assertEqual(1, statsistics['count'])
        self.assertEqual(-1, statsistics['netprofit'])
        self.assertEqual(-1, statsistics['avg'])

if __name__ == '__main__':
    unittest.main()
