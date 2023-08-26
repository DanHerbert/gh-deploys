"""App to handle Github webhooks."""

import logging
import shlex
import subprocess

from flask import Flask, abort, request
from flask.logging import default_handler
from github_webhook import Webhook

from .config import get_config


STARTUP_CONFIG = get_config()
app = Flask(__name__)
app.logger.setLevel(STARTUP_CONFIG.log_level)

webhookLogger = logging.getLogger('webhook')
webhookLogger.setLevel(app.logger.getEffectiveLevel())
webhookLogger.addHandler(default_handler)

webhook = Webhook(app, endpoint=f'{STARTUP_CONFIG.root_path}/postreceive')


def find_project_match(repo_name):
    """Look for matching project in the config."""
    for proj in get_config().projects:
        if proj.repo_name == repo_name:
            return proj
    return None


@app.route('/')
@app.route(STARTUP_CONFIG.root_path)
@app.route(f'{STARTUP_CONFIG.root_path}/')
def root_path_handler():
    """Handle requests to root page to show proof of life in testing."""
    app.logger.info(f'Root path request {request.url}')
    return 'It works!'


@app.errorhandler(404)
def page_not_found():
    """Custom 404 to make diagnosing bad routes easier."""
    app.logger.info(f'Not found request {request.url}')
    return 'Not found!'


@webhook.hook(event_type='push')
def on_push(data):
    """Handle Github push events."""
    repo_name = data['repository']['full_name']
    pushed_ref = data['ref']
    app.logger.info(f'Push to {repo_name} with {pushed_ref}')
    project = find_project_match(repo_name)
    if project is not None:
        desired_ref = f'refs/heads/{project.deploy_branch}'
        if desired_ref == pushed_ref:
            for cmd in project.commands:
                app.logger.debug('Running configured command: ')
                app.logger.debug(cmd)
                result = subprocess.run(shlex.split(cmd),
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        text=True,
                                        timeout=180,
                                        check=False)
                if result.returncode != 0:
                    app.logger.warn(
                        f'Command failure output:\n{result.stdout}')
                    app.logger.error(f'Command failed for {repo_name} on '
                                     f'{pushed_ref}')
                    abort(500, 'Hook action failed')
                else:
                    app.logger.info(
                        f'Command success output:\n{result.stdout}')
                    app.logger.info(f'Successfully ran command for {repo_name} '
                                    f'on {pushed_ref}')
        else:
            app.logger.info(f'Doing nothing. Pushed ref ({pushed_ref}) is '
                            f'not the desired ref ({desired_ref})')
    else:
        app.logger.warn(f'No project capable of handing repo: {repo_name}')
        abort(500, 'Unrecognized repository')


@webhook.hook(event_type='ping')
def on_ping(data):
    """Handle Github ping events."""
    repo_name = data['repository']['full_name']
    app.logger.info(f'Received ping for {repo_name}')
    project = find_project_match(repo_name)

    if project is not None:
        app.logger.info('Config has project ready for pushes.')
    else:
        app.logger.warn(f'No project exists in config for {repo_name}')


# This only happens if running the script directly. Flask/gunicorn will ignore.
if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=STARTUP_CONFIG.debug_listen_port,
            debug=STARTUP_CONFIG.debug_mode)
