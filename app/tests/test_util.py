import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.utils import *
import unittest


class TestUtils(unittest.TestCase):

    def test_is_float(self):
        self.assertTrue(is_float(5.5))
        self.assertTrue(is_float(0.6))
        self.assertTrue(is_float(5))
        self.assertTrue(is_float('5.6'))
        self.assertFalse(is_float('hello'))

    # def test_portfolio(self):
    #     mock_data = [('Ethereum', 'ETH', 4.0), ('Stellar', 'XLM', 76.0)]
    #     expected_data =