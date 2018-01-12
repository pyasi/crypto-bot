from configparser import ConfigParser
from flask import Flask, jsonify, request
from crypto_bot import CryptoBot
from slack import Slack


# Instantiate our Node
app = Flask(__name__)


# Configure Slack Bot
config = ConfigParser()
config.read('../config.ini')
slack_webhook_url = config['slack']['webhook_url']

slack_bot = CryptoBot(slack_webhook_url)
slack = Slack()

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
    response = ''

    if 'help' in command:
        response = slack_bot.create_help_request()
    elif 'coins' in command:
        response = slack_bot.get_list_of_coins()

    #TODO fix this up
    slack.chat(response, channel)

    return '', 200


@app.route('/coin', methods=['POST', 'GET'])
def send_coin_information():
    """
    Slack slash command to get details for a specific coin.
    Command expects a coin ticker value
    :return:
    """
    value = request.form
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