import requests
import json


class Slack(object):

    def __init__(self):
        self.api_token = json.load(open('../local.json'))['slack_api_token']

    def chat(self, message: dict, channel):
        url = 'https://slack.com/api/chat.postMessage'
        headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.api_token)}
        message['channel'] = channel
        response = requests.post(url, data=json.dumps(message), headers=headers)
        response_object = json.loads(response.text)
        if response_object['ok'] == False:
            raise Exception('Failed to send slack- message {}'.format(response_object['error']))
        time_stamp = response_object['ts']
        return time_stamp

    def update_message(self, message, time_stamp, channel):
        """

        :param message:
        :param time_stamp:
        :return:
        """
        url = 'https://slack.com/api/chat.update'
        headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.api_token)}
        message['ts'] = time_stamp
        message['channel'] = channel
        response = requests.post(url, data=json.dumps(message), headers=headers)
        response_object = json.loads(response.text)
        if response_object['ok'] == 'false':
            raise Exception('Failed to send slack- message {}'.format(response_object['error']))
