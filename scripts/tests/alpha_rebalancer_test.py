import unittest
from scripts.alpha_rebalancer import get_alpha_modules
from exobuilder.data.exostorage import EXOStorage


from scripts.settings import *

class AlphaRebalancerTestCase(unittest.TestCase):
    def test_get_alphas_modules(self):
        exo_storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)

        exo_names = exo_storage.exo_list()

        result = get_alpha_modules('..', exo_names)

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
