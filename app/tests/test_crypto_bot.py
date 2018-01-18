import sys
import os
sys.path.insert(0,
                os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '../..')))
from app.crypto_bot import *
import unittest


class TestCryptoBot(unittest.TestCase):

    def setUp(self):
        self.bot = CryptoBot()

    def test_sending_error(self):
        message = 'This is an error'
        expected_value = {'response_type': "ephemeral", 'text': message}
        error = self.bot.create_error(message)
        self.assertEqual(error, expected_value)

    def test_single_coin_upper(self):
        eth = 'ETH'
        single_eth = self.bot.handle_request_for_coin(eth)
        self.assertIsNotNone(single_eth['text'])
        self.assertIsNotNone(single_eth['attachments'])
        self.assertIsNotNone(single_eth['attachments'][0]['fields'])
        self.assertIsNotNone(single_eth['attachments'][0]['color'])
        self.assertIsNotNone(single_eth['attachments'][0]['fallback'])

    def test_single_coin_invalid(self):
        coin = 'invalid'
        expected_error = {'response_type': 'ephemeral', 'text': 'That does not seem to be a valid ticker, try */coin* BTC'}
        invalid_coin = self.bot.handle_request_for_coin(coin)
        self.assertEqual(invalid_coin, expected_error)

    def test_help_request(self):
        help_request = self.bot.create_help_request()
        self.assertIsNotNone(help_request['text'])

    def test_get_all_coins(self):
        coins = self.bot.get_list_of_coins(limit=10)
        self.assertEqual(coins['attachments'][0]['title'], 'Coins and tickers')
        self.assertIsNotNone(coins['attachments'][0]['text'], str)
