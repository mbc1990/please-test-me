import unittest
from project import product

class AdditionTest(unittest.TestCase):

    def test_addition(self):
        res = product.add(2,3)
        self.assertEqual(res, 5)

    def test_negative_addition(self):
        res = product.add(-3,-8)
        self.assertEqual(res, -11)
       

class SubtractionTest(unittest.TestCase):

    def test_subtraction(self):
        res = product.subtract(8,2)
        self.assertEqual(res, 6)
