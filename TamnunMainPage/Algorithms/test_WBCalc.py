""" Integration tests for the W&B algorithms"""

import unittest
import json
import numpy as np
import scipy
import matplotlib as mpl
import WBCalc


class WBtest(unittest.TestCase):
    def test_one(self):
        with open(
            "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\dummyClientExample.json",
            "r",
        ) as f:
            items = json.load(f)

        WB = WBCalc.perform_WB_calc(items)

        with open(
            "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\WBTest1.json",
            "w",
        ) as f:
            f.write(str(json.dumps(DerivativeList)))

        self.assertTrue(True)

    @unittest.skip("Not needed")
    def test_two(self):
        # with open(
        #     "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\dummyClientRequest1.json",
        #     "r",
        # ) as f:
        #     items = json.load(f)

        # DerivativeList = DerivativeGrenerator.Derivative_Grenerator(items)

        # with open(
        #     "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\DerivativeGeneratorTest2.json",
        #     "w",
        # ) as f:
        #     f.write(str(json.dumps(DerivativeList)))

        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
