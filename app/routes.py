from app.utils import *
from flask import request, jsonify
from threading import Thread
import requests
import json
from app import app, slack_bot, slack, database


@app.route('/', methods=['GET'])
def hello():
    return 'hello', 200


@app.route('/mentions', methods=['POST'])
def respond_to_mentions():

    values = request.get_json()

    try:
        message_type = values['event']['subtype']
        if message_type == 'bot_message':
            return '', 204
    except KeyError:
        pass

    command = values['event']['text'].lower()
    channel = values['event']['channel']
    user = values['event']['user']

    if 'help' in command:
        message_to_slack = slack_bot.create_help_request()
        return slack.post_message(message_to_slack, channel), 200
    elif 'coins' in command:
        message_to_slack = slack_bot.get_list_of_coins()
        return slack.post_message(message_to_slack, channel), 200
    elif 'portfolio' in command:
        worker_thread = Thread(target=process_portfolio, args=[user, channel])
        worker_thread.run()
        return (jsonify({"response_type": "in_channel"}), 200) if worker_thread.is_alive() else '', 200

    return '', 204

# TODO no current action to respond to in app, ephemeral messages don't have 'original_message' :sad:
@app.route('/post/actions', methods=['POST'])
def respond_to_actions():

    values = json.loads(request.values['payload'])
    #original_message = values['original_message']
    channel = values['channel']['id']
    time_stamp = values['message_ts']

    if values['actions'][0]['value'] == 'publish':
        #original_message['response_type'] == 'in_channel'
        slack.update_message(time_stamp, channel)

    return '', 204


@app.route('/portfolio', methods=['POST', 'GET'])
def add_to_portfolio():

    worker_thread = Thread(target=process_portfiolio_command, args=[request])
    worker_thread.run()

    return (jsonify({"response_type": "in_channel"}), 200) if worker_thread.is_alive() else '', 204


def process_portfiolio_command(value_form):

    user = value_form.form.get('user_id')
    text = value_form.form.get('text', None)
    channel = value_form.form.get('channel_id', None)
    response_url = value_form.form.get("response_url")

    if text == "":
        process_portfolio(user, channel)
        return


    values = text.split(' ')
    coin = slack_bot.coincap.get_coin_detail(values[0].upper())
    if not coin or len(values) != 2 or not is_float(values[1]):
        response = slack_bot.create_error(
            'That was not a valid portfolio entry')
        slack.post_ephemeral(response, channel, user)
        return '', 204

    entry = dict(
        username=user,
        coin=coin['display_name'],
        ticker=coin['id'],
        amount=values[1])
    print(entry['amount'])
    if entry['amount'] is '0':
        database.delete_coin(entry)
    else:
        database.enter_coin(entry)
    data = database.get_user_portfolio(user)
    portfolio = create_portfolio(data)

    response = slack_bot.create_portfolio(portfolio)
    requests.post(response_url, json=response)


def process_portfolio(user, channel):
    data = database.get_user_portfolio(user)
    portfolio = create_portfolio(data)
    response = slack_bot.create_portfolio(portfolio)
    slack.post_ephemeral(response, channel, user)


@app.route('/coin', methods=['POST', 'GET'])
def send_coin_information():

    worker_thread = Thread(target=process_coin_command, args=[request])
    worker_thread.run()

    return (jsonify({"response_type": "in_channel"}), 200) if worker_thread.is_alive() else '', 200


def process_coin_command(value_form):

    text = value_form.form.get('text', None).split(' ')
    channel = value_form.form.get('channel_id', None)
    response_url = value_form.form.get('response_url')

    response = slack_bot.handle_request_for_coin(text[0].upper())

    if len(text) > 1 and text[1] == 'public':
        slack.post_message(response, channel)
    else:
        requests.post(response_url, json=response)

