from app.utils import *
from app import app, slack_bot, slack, database
from flask import request, jsonify
import json


@app.route('/mentions', methods=['POST'])
def respond_to_mentions():

    values = request.get_json()
    try:
        message_type = values['event']['subtype']
        if message_type == 'bot_message':
            return '', 204
    except KeyError:
        pass

    command = values['event']['text']
    channel = values['event']['channel']
    user = values['event']['user']

    if 'help' in command:
        response = slack_bot.create_help_request()
        slack.post_message(response, channel)
    elif 'coins' in command:
        response = slack_bot.get_list_of_coins()
        slack.post_message(response, channel)
    elif 'portfolio' in command:
        data = database.get_user_portfolio(user)
        portfolio = create_portfolio(data)
        response = slack_bot.create_portfolio(portfolio)
        slack.post_ephemeral(response, channel, user)

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

    user = request.form.get('user_id')
    text = request.form.get('text', None)
    channel = request.form.get('channel_id', None)

    values = text.split(' ')
    coin = slack_bot.coincap.get_coin_detail(values[0].upper())
    if not coin or not is_float(values[1]):
        response = slack_bot.create_error(
            'That was not a valid portfolio entry')
        slack.post_ephemeral(response, channel, user)
        return '', 200

    entry = dict(
        username=user,
        coin=coin['display_name'],
        ticker=coin['id'],
        amount=values[1])
    database.enter_coin(entry)
    data = database.get_user_portfolio(user)
    portfolio = create_portfolio(data)

    response = slack_bot.create_portfolio(portfolio)
    return jsonify(response), 200


@app.route('/coin', methods=['POST', 'GET'])
def send_coin_information():

    text = request.form.get('text', None).split(' ')
    channel = request.form.get('channel_id', None)

    response = slack_bot.handle_request_for_coin(text[0].upper())

    if len(text) > 1 and text[1] == 'public':
        slack.post_message(response, channel)
        return '', 204

    return jsonify(response), 200
