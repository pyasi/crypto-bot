from coincap import CoinCap

AVAILABLE_CURRENCIES = ['usd', 'eur', 'btc', 'ltc', 'zec', 'eth']


class CryptoBot(object):

    def __init__(self, currency='usd'):
        self.coincap = CoinCap()
        if currency.lower() in AVAILABLE_CURRENCIES:
            self.currency = currency.lower()
        else:
            # Fallback to USD
            self.currency = 'usd'

    def _create_error(self, message):
        """
        Create the JSON object for an error response to the user
        """
        payload = {'response_type': "ephemeral", 'text': message}
        return payload

    def _single_coin_post(self, coin_ticker):
        """
        Create a JSON object with an attachment giving the details of a
        single coin
        """
        coin = self.coincap.get_coin_detail(coin_ticker)
        if coin:
            payload = {
                'text':
                '*<http://coincap.io/{}|{}>* - ({})\n\n*Current Price: ${:0.5f}*'.
                format(coin['id'], coin['display_name'], coin['id'],
                       coin['price_' + self.currency]),
                'attachments':
                [self._create_attachment_with_coin_details(coin)]
            }
            return payload
        else:
            return self._create_error(
                'That does not seem to be a valid ticker, try */coin* BTC')

    def _create_attachment_with_coin_details(self, coin):
        """
        Creates the attachment for a single coin query
        """
        attachment = {
            'fallback':
            '{}, current price: {}, 24 hour change: {}'.format(
                coin['display_name'], coin['price_' + self.currency],
                coin['cap24hrChange']),
            'color':
            '#008000' if coin['cap24hrChange'] > 0 else '#FF0000',
            'fields': [{
                'value':
                '*24 Hour Change:* {:>}%\n'.format(str(coin['cap24hrChange'])),
                'short':
                'false'
            }, {
                'value':
                '*Market Cap:* ${:,}\n'.format(coin['market_cap']),
                'short':
                'false'
            }, {
                'value':
                '*24 Hour Volume:* ${:,}\n'.format(coin['volume']),
                'short':
                'false'
            }, {
                'value':
                '*Available Supply:* {:,}\n'.format(coin['supply']),
                'short':
                'false'
            }]
        }
        return attachment

    # TODO Currently Unused
    def _create_publish_to_channel_action(self):
        """
        Create an action (button) to publish a particular message to the channel
        """
        attachment = {
            'color':
            '#D3D3D3',
            'callback_id':
            'publish_to_channel',
            "actions": [{
                "name": "Publish",
                "text": "Publish to Channel  :eyes:",
                "type": "button",
                "value": "publish"
            }]
        }
        return attachment

    def _create_portfolio_for_coins(self, portfolio):
        """
        Create a potfolio JSON object to display users portfolio

        :param portfolio: A list of Coins and the amount the user holds
        :return: JSON object
        """
        total_amount = 0
        for coin in portfolio:
            current_coin = self.coincap.get_coin_detail(coin.ticker)
            total_amount = total_amount + (
                current_coin['price_{}'.format(self.currency)] * coin.amount)

        payload = {
            'text': '*Portfolio* - ${:0,.2f}'.format(total_amount),
            'attachments': self._create_attachments_for_portfolio(portfolio)
        }
        return payload

    def _create_attachments_for_portfolio(self, portfolio):
        """
        Create an attachment for the portfolio.
        """
        attachments = []
        if len(portfolio) == 0:
            attachment = {
                'fallback':
                'portfolio coin',
                'color':
                '#D3D3D3',
                'fields': [{
                    'value':
                    'Your portfolio is empty, fill it with the */portfolio* command!',
                    'short':
                    'false'
                }]
            }
            return [attachment]
        for coin in portfolio:
            current_coin = self.coincap.get_coin_detail(coin.ticker)
            attachment = {
                'fallback':
                'portfolio coin',
                'color':
                '#D3D3D3',
                'title':
                '{}: - '.format(current_coin['display_name']) +
                '${0:,.5f}'.format(current_coin['price_{}'.format(
                    self.currency)]),
                'title_link':
                'http://coincap.io/{}'.format(current_coin['id']),
                'fields': [{
                    'value':
                    '{:0.5f} {}:   '.format(
                        int(coin.amount)
                        if coin.amount.is_integer() else coin.amount,
                        current_coin['id']) + ' ${:0,.2f}\n'.format(
                            coin.amount * current_coin['price_{}'.format(
                                self.currency)]),
                    'short':
                    'false'
                }]
            }
            attachments.append(attachment)
        return attachments

    def get_list_of_coins(self, limit=None):
        """
        Create a JSON object containing a list of coins and their corresponding tickers
        """
        coins = []
        top_coins = self.coincap.get_front()[:limit]
        response_string = "\n"
        for coin in top_coins:
            coins.append([coin['long'], coin['short']])
            response_string = response_string + '{} - `{}` *|* '.format(
                coin['long'], coin['short'])

        payload = {
            'attachments': [{
                "fallback": "List of coins",
                "color": "#008000",
                "text": response_string,
                "title": "Coins and tickers",
            }]
        }
        return payload

    def create_help_request(self):
        """
        Create a JSON object to respond to a help request, explain functionality.
        """
        payload = {
            "text":
            "You can ask me things like \n"
            "*@cryptobot coins* - shows list of coin tickers\n"
            "*@cryptobot portfolio* - show your personal portfolio\n"
            "or use my slash commands: \n"
            "*/coin* to show stats on any coin\n"
            "*/portfolio* to add to your personal portfolio for real time tracking!",
            "mrkdw":
            "true"
        }
        return payload

    def create_error(self, message):
        """
        Creates an error with text of your choosing

        :param message: text to send to user
        :return: JSON object
        """
        return self._create_error(message)

    def handle_request_for_coin(self, coin_ticker):
        """
        Creates post for single coin statistics
        """
        return self._single_coin_post(coin_ticker)

    def create_portfolio(self, portfolio):
        """
        Creates a post for the user's portfolio

        :param portfolio: list of Coins
        :return: JSON object
        """
        return self._create_portfolio_for_coins(portfolio)
