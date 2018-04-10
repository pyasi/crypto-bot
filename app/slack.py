import requests
import json
import os


class Slack(object):

    def post_to_slack(self, url, message, channel, token):
        """
        Generic method to post any given content to slack

        :param url: slack URL to hit
        :param message: message contents as a JSON object
        :param channel: channel id to post to
        :return: timestamp of sent message
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }
        message['channel'] = channel
        response = requests.post(
            url, data=json.dumps(message), headers=headers)
        response_object = json.loads(response.text)
        if response_object['ok'] is False:
            return 'Failed to send slack- message {}'.format(response_object['error'])
        try:
            time_stamp = response_object['ts']
            return time_stamp
        except KeyError:
            return

    def post_message(self, message, channel, token):
        """
        Create a public post using Slack's API

        :param message: message contents as a JSON object
        :param channel: channel id to post to
        :return: timestamp of message
        """
        url = 'https://slack.com/api/chat.postMessage'
        return self.post_to_slack(url, message, channel, token)

    def post_ephemeral(self, message, channel, user, token):
        """
        Create a private (ephemeral) message using Slack's API

        :param message: message contents as a JSON object
        :param channel: channel id to post to
        :return: timestamp of message
        """
        url = 'https://slack.com/api/chat.postEphemeral'
        message['user'] = user
        return self.post_to_slack(url, message, channel, token)

    def update_message(self, message, time_stamp, channel):
        """
        Update an existing message using Slack's API

        :param message: message contents as a JSON object
        :param time_stamp: timestamp of message to update
        :return: timestamp of message
        """
        url = 'https://slack.com/api/chat.update'
        message['ts'] = time_stamp
        return self.post_to_slack(url, message, channel)
