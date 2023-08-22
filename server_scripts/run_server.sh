#!/bin/sh

set -ev

cd /home/dan/code/gh-deploys/
./env/bin/gunicorn 'gh_deploys:app'
