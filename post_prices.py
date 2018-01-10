from configparser import ConfigParser
from coincap import CoinCap
import requests
import json

AVAILABLE_CURRENCIES = ['usd', 'eur', 'btc', 'ltc', 'zec', 'eth']

class SlackBot(object):

    def __init__(self, webhook_url, currency='usd'):
        self.webhook_url = webhook_url
        self.coincap = CoinCap()
        if currency.lower() in AVAILABLE_CURRENCIES:
            self.currency = currency.lower()
        else:
            # Fallback to USD
            self.currency = 'usd'

    def _post_slack_message(self, payload, channel='#test-bot'):
        """Post message to a slack channel
        :param string webhook_url: required webhook url to use
        :param string msg: Message to post
        :param string channel: Optional channel to post to (by default will use webhook's) Should be full channel '#example' or '@username'
        """
        if channel:
            payload['channel'] = channel
        else:
            print('oops')
        requests.post(self.webhook_url, json=payload)

    def _create_coin_post(self):
        """

        """
        coin = self.coincap.get_coin_detail('ETH')
        print(coin)
        payload = {}
        payload['attachments'] = [self._create_attachment_with_coin_details(coin)]
        self._post_slack_message(payload)

    def _create_top_coins_post(self):
        """
        """


    def _create_attachment_with_coin_details(self, coin):
        """
        """
        attachment = {
            'fallback': '{}, current price: {}, 24 hour change: {}'.format(
                coin['display_name'], coin['price_' + self.currency], coin['cap24hrChange']),
            'color': '#008000' if coin['cap24hrChange'] > 0 else '#FF0000',
            'title': coin['display_name'],
            'fields': [
                {
                    'title': 'Current Price',
                    'value': coin['price_' + self.currency],
                    'short': 'false'
                },
                {
                    'title': '24 Hour Change',
                    'value': coin['cap24hrChange'],
                    'short': 'false'
                }
                    ],
            'ts': 123456789
            }

        return attachment



    def post(self):
        """

        """
        self._create_coin_post()


def main():
    config = ConfigParser()
    config.read('config.ini')
    slack_webhook_url = config['slack']['webhook_url']
    bot = SlackBot(slack_webhook_url)
    bot.post()


if __name__ == "__main__":
    main()
