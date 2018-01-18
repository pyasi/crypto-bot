import sys
import os
sys.path.insert(0,
                os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '../..')))
from app.routes import app
import unittest
import json


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    # Main page
    def test_front_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # /mentions route
    def test_mentions_portfolio(self):
        response = test_mention(self.app, 'portfolio')
        self.assertEqual(response.status_code, 200)

    def test_mentions_help(self):
        response = test_mention(self.app, 'help')
        self.assertEqual(response.status_code, 200)

    def test_mentions_coins(self):
        response = test_mention(self.app, 'coins')
        self.assertEqual(response.status_code, 200)

    def test_mentions_other(self):
        response = test_mention(self.app, 'not a valid mention')
        self.assertEqual(response.status_code, 204)

    # /portfolio route

    # def test_slash_command_portfolio(self):
    #     data = [
    #         ('trigger_id', '300570783460.96216496371.851b4c60f3a31f9857321cb5ceef8149'),
    #         ('channel_id', 'D8QFT1BA6'), ('user_name', 'peewhy-chubz'),
    #         ('token', 'n2AGYIKrSxZ2piTimgTokS99'), ('team_id', 'T2U6CELAX'),
    #         ('channel_name', 'directmessage'),
    #         ('user_id', 'U2U8FE8TE'),
    #         ('team_domain', 'theboocrew'),
    #         ('command', '/portfolio'),
    #         ('response_url', 'https://hooks.slack.com/commands/T2U6CELAX/300702049109/9I6XHNm0r30JVFH9O3trBtcs'),
    #         ('text', 'eth')
    #     ]
    #     response = self.app.post(
    #         '/portfolio',
    #         data=data,
    #         content_type='application/x-www-form-urlencoded')
    #     self.assertEqual(response.status_code, 200)


# Helper methods


def test_mention(test_app, message):
    data = {
        'event': {
            'text': '{}'.format(message),
            'ts': '1516229465.000148',
            'type': 'message',
            'user': 'any_user',
            'channel': 'any-channel'
        }
    }
    return test_app.post(
        '/mentions', data=json.dumps(data), content_type='application/json')
