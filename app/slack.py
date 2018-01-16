import requests
import json


class Slack(object):
    def __init__(self):
        self.api_token = json.load(open('../local.json'))['slack_api_token']

    def post_to_slack(self, url, message, channel):
        """

        :param url:
        :return:
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.api_token)
        }
        message['channel'] = channel
        response = requests.post(
            url, data=json.dumps(message), headers=headers)
        response_object = json.loads(response.text)
        if response_object['ok'] is False:
            raise Exception('Failed to send slack- message {}'.format(
                response_object['error']))
        try:
            time_stamp = response_object['ts']
            return time_stamp
        except KeyError:
            return

    def post_message(self, message: dict, channel):
        """

        :param message:
        :param channel:
        :return:
        """
        url = 'https://slack.com/api/chat.postMessage'
        return self.post_to_slack(url, message, channel)

    def post_ephemeral(self, message: dict, channel, user):
        """

        :param message:
        :param channel:
        :return:
        """
        url = 'https://slack.com/api/chat.postEphemeral'
        message['user'] = user
        return self.post_to_slack(url, message, channel)

    def update_message(self, message, time_stamp, channel):
        """

        :param message:
        :param time_stamp:
        :return:
        """
        url = 'https://slack.com/api/chat.update'
        message['ts'] = time_stamp
        return self.post_to_slack(url, message, channel)
