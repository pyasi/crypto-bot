from configparser import ConfigParser
from crypto_bot import CryptoBot
from flask import Flask, jsonify, request

# Instantiate our Node
app = Flask(__name__)


# Configure Slack Bot
config = ConfigParser()
config.read('config.ini')
slack_webhook_url = config['slack']['webhook_url']

# Instantiate the Blockchain
slack_bot = CryptoBot(slack_webhook_url)

@app.route('/mentions', methods=['POST'])
def respond_to_mentions():
    print(request)
    values = request.get_json()

    print(values['event']['text'])

    #if 'help' in values['event']['text']:

    return jsonify(values), 200


@app.route('/coin', methods=['POST', 'GET'])
def send_coin_information():
    """
    Slack slash command to get details for a specific coin.
    Command expects a coin ticker value
    :return:
    """
    command = request.form.get('command', None)
    text = request.form.get('text', None)

    response = slack_bot.handle_request(text.upper())
    print('about to send {}'.format(response))
    return jsonify(response)

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
