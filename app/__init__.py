from flask import Flask
from app.crypto_bot import CryptoBot
from app.slack import Slack
from app.database import Database

app = Flask(__name__)

slack_bot = CryptoBot()
slack = Slack()
database = Database('crypto_portfolio')

from app import routes
