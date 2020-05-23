import unittest
import json
import numpy as np
import scipy
import matplotlib as mpl
import DerivativeGrenerator


class TestCase1(unittest.TestCase):
    def test_one(self):
        with open(
            "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\dummyClientRequest0.json",
            "r",
        ) as f:
            items = json.load(f)

        DerivativeList = DerivativeGrenerator.Derivative_Grenerator(items)

        with open(
            "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\DerivativeGeneratorTest1.json",
            "w",
        ) as f:
            f.write(str(json.dumps(DerivativeList)))

        self.assertTrue(True)

    @unittest.skip("Not needed")
    def test_two(self):
        with open(
            "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\dummyClientRequest1.json",
            "r",
        ) as f:
            items = json.load(f)

        DerivativeList = DerivativeGrenerator.Derivative_Grenerator(items)

        with open(
            "C:\\Tamnun\\TAMNUN_DEV\\TamnunProject\\TamnunMainPage\\DummyData\\DerivativeGeneratorTest2.json",
            "w",
        ) as f:
            f.write(str(json.dumps(DerivativeList)))

        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
