import unittest
from exobuilder.algorithms.rollover_helper import RolloverHelper
from datetime import datetime



class DummyContract:
    def __init__(self, _dict):
        self._dict = _dict
        self.name = _dict['name']
        self.to_expiration_days = _dict['days']
        self.expiration = _dict['expiration']

        if 'options' in _dict:
            self.options = [DummyContract(opt) for opt in _dict['options']]


class DummyInstrument:
    def __init__(self, _dict):
        self.name = _dict['name']
        if 'futures' in _dict:
            self.futures = [DummyContract(fut) for fut in _dict['futures']]
        else:
            raise NotImplementedError("_dict must have 'futures")


class RolloverHelperTestCase(unittest.TestCase):
    def test_init(self):
        inst_dict = {
            'name': 'TEST',
            'futures': [
                {
                    'days': 5,
                    'name': 'fut1',
                    'expiration': datetime(2015, 1, 10),
                    'options': [
                        {
                            'days': 3,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut1_opt1'
                        },
                    ]
                }
            ]

        }

        dinst = DummyInstrument(inst_dict)
        rh = RolloverHelper(dinst)

        self.assertEqual(2, rh.days_before_expiration)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], rh.rollover_months)

    def test_dummyinstument(self):
        inst_dict = {
            'name': 'TEST',
            'futures':     [
                {
                    'days': 5,
                    'name': 'fut1',
                    'expiration': datetime(2015, 1, 10),
                    'options': [
                        {
                            'days': 3,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut1_opt1'
                        },
                    ]
                }
            ]

        }

        dinst = DummyInstrument(inst_dict)
        self.assertEqual('fut1', dinst.futures[0].name)
        self.assertEqual('fut1_opt1', dinst.futures[0].options[0].name)

    def test_active_chains_current(self):
        inst_dict = {
            'name': 'TEST',
            'futures': [
                {
                    'days': 5,
                    'name': 'fut1',
                    'expiration': datetime(2015, 1, 10),
                    'options': [
                        {
                            'days': 3,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut1_opt1'
                        },
                    ]
                }
            ]

        }

        dinst = DummyInstrument(inst_dict)
        rh = RolloverHelper(dinst)

        fut, opt = rh.get_active_chains()
        self.assertEqual(fut.name, 'fut1')
        self.assertEqual(opt.name, 'fut1_opt1')

    def test_active_chains_rollover_month_custom(self):
        inst_dict = {
            'name': 'TEST',
            'futures': [
                {
                    'days': 5,
                    'name': 'fut1',
                    'expiration': datetime(2015, 1, 10),
                    'options': [
                        {
                            'days': 3,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut1_opt1'
                        },
                    ]
                },
                {
                    'days': 20,
                    'name': 'fut2',
                    'expiration': datetime(2015, 2, 10),
                    'options': [
                        {
                            'days': 20,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut2_opt1'
                        },
                    ]
                },
                {
                    'days': 40,
                    'name': 'fut3',
                    'expiration': datetime(2015, 3, 10),
                    'options': [
                        {
                            'days': 40,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut3_opt1'
                        },
                    ]
                }
            ]

        }

        dinst = DummyInstrument(inst_dict)
        rh = RolloverHelper(dinst)
        rh.rollover_months = [1, 3]
        rh.days_before_expiration = 10

        fut, opt = rh.get_active_chains()
        self.assertEqual(fut.name, 'fut3')
        self.assertEqual(opt.name, 'fut3_opt1')

    def test_active_chains_rollover_inside_options(self):
        inst_dict = {
            'name': 'TEST',
            'futures': [
                {
                    'days': 20,
                    'name': 'fut1',
                    'expiration': datetime(2015, 1, 10),
                    'options': [
                        {
                            'days': 3,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut1_opt1'
                        },
                        {
                            'days': 30,
                            'expiration': datetime(2015, 2, 8),
                            'name': 'fut1_opt2'
                        },
                    ]
                },
                {
                    'days': 20,
                    'name': 'fut2',
                    'expiration': datetime(2015, 2, 10),
                    'options': [
                        {
                            'days': 20,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut2_opt1'
                        },
                    ]
                },
                {
                    'days': 40,
                    'name': 'fut3',
                    'expiration': datetime(2015, 3, 10),
                    'options': [
                        {
                            'days': 40,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut3_opt1'
                        },
                    ]
                }
            ]

        }

        dinst = DummyInstrument(inst_dict)
        rh = RolloverHelper(dinst)
        rh.rollover_months = [1, 3]
        rh.days_before_expiration = 10

        fut, opt = rh.get_active_chains()
        self.assertEqual(fut.name, 'fut1')
        self.assertEqual(opt.name, 'fut1_opt2')

    def test_active_chains_rollover_options_for_next_series(self):
        inst_dict = {
            'name': 'TEST',
            'futures': [
                {
                    'days': 20,
                    'name': 'fut1',
                    'expiration': datetime(2015, 1, 10),
                    'options': [
                        {
                            'days': 3,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut1_opt1'
                        },
                    ]
                },
                {
                    'days': 20,
                    'name': 'fut2',
                    'expiration': datetime(2015, 2, 10),
                    'options': [
                        {
                            'days': 20,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut2_opt1'
                        },
                    ]
                },
                {
                    'days': 40,
                    'name': 'fut3',
                    'expiration': datetime(2015, 3, 10),
                    'options': [
                        {
                            'days': 4,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut3_opt1'
                        },
                        {
                            'days': 60,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut3_opt2'
                        },
                    ]
                }
            ]

        }

        dinst = DummyInstrument(inst_dict)
        rh = RolloverHelper(dinst)
        rh.rollover_months = [1, 3]
        rh.days_before_expiration = 10

        fut, opt = rh.get_active_chains()
        self.assertEqual(fut.name, 'fut3')
        self.assertEqual(opt.name, 'fut3_opt2')

    def test_active_chains_rollover_options_for_next_expiration(self):
        inst_dict = {
            'name': 'TEST',
            'futures': [
                {
                    'days': 20,
                    'name': 'fut1',
                    'expiration': datetime(2015, 1, 10),
                    'options': [
                        {
                            'days': 3,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut1_opt1'
                        },
                        {
                            'days': 3,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut1_opt2'
                        },
                        {
                            'days': 30,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut1_opt3'
                        },
                    ]
                },
                {
                    'days': 20,
                    'name': 'fut2',
                    'expiration': datetime(2015, 2, 10),
                    'options': [
                        {
                            'days': 20,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut2_opt1'
                        },
                    ]
                },
                {
                    'days': 40,
                    'name': 'fut3',
                    'expiration': datetime(2015, 3, 10),
                    'options': [
                        {
                            'days': 4,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut3_opt1'
                        },
                        {
                            'days': 60,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut3_opt2'
                        },
                    ]
                }
            ]

        }

        dinst = DummyInstrument(inst_dict)
        rh = RolloverHelper(dinst)
        rh.rollover_months = [1, 3]
        rh.days_before_expiration = 10

        fut, opt = rh.get_active_chains()
        self.assertEqual(fut.name, 'fut1')
        self.assertEqual(opt.name, 'fut1_opt3')

    def test_active_chains_rollover_options_no_options_in_chain(self):
        inst_dict = {
            'name': 'TEST',
            'futures': [
                {
                    'days': 20,
                    'name': 'fut1',
                    'expiration': datetime(2015, 1, 10),
                    'options': []
                },
                {
                    'days': 20,
                    'name': 'fut2',
                    'expiration': datetime(2015, 2, 10),
                    'options': [
                        {
                            'days': 20,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut2_opt1'
                        },
                    ]
                },
                {
                    'days': 40,
                    'name': 'fut3',
                    'expiration': datetime(2015, 3, 10),
                    'options': [
                        {
                            'days': 4,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut3_opt1'
                        },
                        {
                            'days': 60,
                            'expiration': datetime(2015, 1, 8),
                            'name': 'fut3_opt2'
                        },
                    ]
                }
            ]

        }

        dinst = DummyInstrument(inst_dict)
        rh = RolloverHelper(dinst)
        rh.rollover_months = [1, 3]
        rh.days_before_expiration = 10

        fut, opt = rh.get_active_chains()
        self.assertEqual(fut.name, 'fut3')
        self.assertEqual(opt.name, 'fut3_opt2')


    def test_active_chains_rollover_options_no_options_chains(self):
        inst_dict = {
            'name': 'TEST',
            'futures': [
                {
                    'days': 20,
                    'name': 'fut1',
                    'expiration': datetime(2015, 1, 10),
                    'options': []
                },
                {
                    'days': 20,
                    'name': 'fut2',
                    'expiration': datetime(2015, 2, 10),
                    'options': []
                },
                {
                    'days': 40,
                    'name': 'fut3',
                    'expiration': datetime(2015, 3, 10),
                    'options': []
                }
            ]

        }

        dinst = DummyInstrument(inst_dict)
        rh = RolloverHelper(dinst)
        rh.rollover_months = [1, 3]
        rh.days_before_expiration = 10

        fut, opt = rh.get_active_chains()
        self.assertEqual(fut.name, 'fut1')
        self.assertEqual(opt, None)

    def test_active_chains_rollover_options_no_futures(self):
        inst_dict = {
            'name': 'TEST',
            'futures': []
        }

        dinst = DummyInstrument(inst_dict)
        rh = RolloverHelper(dinst)
        rh.rollover_months = [1, 3]
        rh.days_before_expiration = 10

        fut, opt = rh.get_active_chains()
        self.assertEqual(fut, None)
        self.assertEqual(opt, None)

    def test_is_rollover(self):
        inst_dict = {
            'name': 'TEST',
            'futures': []
        }

        dinst = DummyInstrument(inst_dict)
        rh = RolloverHelper(dinst)
        rh.rollover_months = [1, 3]
        rh.days_before_expiration = 10

        contr = DummyContract({
                    'days': 20,
                    'name': 'fut1',
                    'expiration': datetime(2015, 1, 10),
                    'options': []
                })

        self.assertEqual(rh.is_rollover(contr), False)

        contr = DummyContract({
            'days': 10,
            'name': 'fut1',
            'expiration': datetime(2015, 1, 10),
            'options': []
        })

        self.assertEqual(rh.is_rollover(contr), True)

        contr = DummyContract({
            'days': 1,
            'name': 'fut1',
            'expiration': datetime(2015, 1, 10),
            'options': []
        })

        self.assertEqual(rh.is_rollover(contr), True)





if __name__ == '__main__':
    unittest.main()
