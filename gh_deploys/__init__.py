import sys
import logging

from github_webhook import Webhook
from flask import Flask, request
from .config import get_config

config = get_config()
app = Flask(__name__)
app.logger.setLevel(logging.getLevelName(config['log_level']))
webhook = Webhook(app, secret=config['secret'])

@app.route("/")
def root_path_handler():
    app.logger.info(f'Handling {request.url}')
    return "It works!"

@webhook.hook(event_type="push")
def on_push(data):
    app.logger.info(f'Handling {request.url}')
    app.logger.info(f'Got push with: {data}')

if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=config['listen_port'],
            debug=config['debug_mode'])