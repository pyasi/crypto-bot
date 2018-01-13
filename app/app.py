from configparser import ConfigParser
from flask import Flask, jsonify, request
from crypto_bot import CryptoBot
from slack import Slack
from database import Database
from utils import *


# Instantiate our Node
app = Flask(__name__)

# Configure Slack Bot
config = ConfigParser()
config.read('../config.ini')
slack_webhook_url = config['slack']['webhook_url']

slack_bot = CryptoBot(slack_webhook_url)
slack = Slack()

database = Database('crypto_portfolio')

@app.route('/mentions', methods=['POST'])
def respond_to_mentions():
    values = request.get_json()
    try:
        message_type = values['event']['subtype']
        if message_type == 'bot_message':
            return '', 200
    except KeyError:
        pass

    print(values)

    command = values['event']['text']
    channel = values['event']['channel']
    user = values['event']['user']
    response = ''

    if 'help' in command:
        response = slack_bot.create_help_request()
    elif 'coins' in command:
        response = slack_bot.get_list_of_coins()
    elif 'portfolio' in command:
        data = database.get_user_portfolio(user)
        portfolio = create_portfolio(data)
        response = slack_bot.create_portfolio(portfolio)

    slack.chat(response, channel)

    return '', 200

@app.route('/portfolio', methods=['POST', 'GET'])
def add_to_portfolio():
    """

    """
    user = request.form.get('user_id')
    text = request.form.get('text', None)
    channel = request.form.get('channel_id', None)

    values = text.split(' ')
    coin = slack_bot.coincap.get_coin_detail(values[0].upper())
    if not coin or not is_float(values[1]) or not is_float(values[2]):
        response = slack_bot.create_error('That was not a valid portfolio entry')
        slack.chat(response, channel)
        return '', 200

    entry = dict(username=user, coin=coin['display_name'], ticker=coin['id'], amount=values[1], price=values[2])
    database.add_coin(entry)
    data = database.get_user_portfolio(user)
    portfolio = create_portfolio(data)

    response = slack_bot.create_portfolio(portfolio)
    slack.chat(response, channel)
    return '', 200


@app.route('/coin', methods=['POST', 'GET'])
def send_coin_information():
    """

    """
    command = request.form.get('command', None)
    text = request.form.get('text', None)
    channel = request.form.get('channel_id', None)

    response = slack_bot.handle_request_for_coin(text.upper())
    slack.chat(response, channel)
    return '', 200

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
