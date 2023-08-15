"""App to handle Github webhooks."""

import logging

from github_webhook import Webhook
from flask import Flask, request
from .config import get_config

config = get_config()
app = Flask(__name__)
app.logger.setLevel(logging.getLevelName(config['log_level']))
webhook = Webhook(app, endpoint=f'{config["root_path"]}/postreceive')
webhookLogger = logging.getLogger('webhook')
webhookLogger.setLevel(logging.getLevelName(config['log_level']))

@app.route("/")
@app.route(config["root_path"])
@app.route(f'{config["root_path"]}/')
def root_path_handler():
    """Handle requests to root page to show proof of life in testing."""
    app.logger.info(f'Handling {request.url}')
    return "It works!"

@app.errorhandler(404)
def page_not_found():
    """Custom 404 to make diagnosing bad routes easier."""
    app.logger.info(f'Handling {request.url}')
    return "Not found!"

@webhook.hook(event_type="push")
def on_push(data):
    """Handle Github push events."""
    app.logger.info(f'Handling {request.url}')
    app.logger.info(f'Push to {data["repository"]["full_name"]} with {data["ref"]}')

@webhook.hook(event_type="ping")
def on_ping():
    """Handle Github ping events."""
    app.logger.info(f'Handling {request.url}')
    app.logger.info('Got ping request')

# This only happens if running the script directly. Flask/gunicorn ignore this.
if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=config['listen_port'],
            debug=config['debug_mode'])
