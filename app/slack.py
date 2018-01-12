import requests
import json
import os


class Slack(object):

    def __init__(self):
        self.api_token = os.environ.get('SLACK_API_TOKEN', '')

    def chat(self, message: dict, channel):
        url = "https://slack.com/api/chat.postMessage"
        headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.api_token)}
        message['channel'] = channel
        requests.post(url, data=json.dumps(message), headers=headers)
