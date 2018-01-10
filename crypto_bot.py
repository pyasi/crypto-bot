from coincap import CoinCap
import requests

AVAILABLE_CURRENCIES = ['usd', 'eur', 'btc', 'ltc', 'zec', 'eth']


class CryptoBot(object):

    def __init__(self, webhook_url, currency='usd'):
        self.webhook_url = webhook_url
        self.coincap = CoinCap()
        if currency.lower() in AVAILABLE_CURRENCIES:
            self.currency = currency.lower()
        else:
            # Fallback to USD
            self.currency = 'usd'

    def _create_slack_message(self, payload, channel='#test-bot'):
        """Post message to a slack channel

        :param string webhook_url: required webhook url to use
        :param string channel: Optional channel to post to (by default will use webhook's) Should be full channel '#example' or '@username'
        """
        if channel:
            payload['channel'] = channel
        else:
            #TODO tidy up
            print('oops')
        return payload

    def _respond_with_error(self, message):
        """

        """
        payload = {
            "response_type": "ephemeral",
            'text': message
        }
        return payload

    def _single_coin_post(self, coin_ticker):
        """

        """
        coin = self.coincap.get_coin_detail(coin_ticker)
        if coin:
            payload = {
                "response_type": "in_channel",
                'attachments': [self._create_attachment_with_coin_details(coin)]
            }
            return self._create_slack_message(payload)
        else:
            print('erroring')
            return self._respond_with_error('That does not seem to be a valid ticker')


    def _top_coins_post(self, limit=10):
        """

        """
        coins = self.coincap.get_front()[:limit]
        list_of_attachments = []
        for coin in coins:
            list_of_attachments.append(self._create_attachment_with_coin_details_from_top(coin))
        payload = {
            "response_type": "in_channel",
            'attachments': list_of_attachments
        }
        self._create_slack_message(payload)

    def _create_attachment_with_coin_details_from_top(self, coin):
        """

        """
        attachment = {
            'fallback': '{}, current price: {}, 24 hour change: {}'.format(
                coin['long'], coin['price'], coin['cap24hrChange']),
            'color': '#008000' if coin['cap24hrChange'] > 0 else '#FF0000',
            'title': coin['long'],
            'fields': [
                {
                    'title': 'Current Price',
                    'value': coin['price'],
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


    def handle_request(self, coin_ticker):
        """

        """
        return self._single_coin_post(coin_ticker)
