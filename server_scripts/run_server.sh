#!/bin/sh


SCRIPT_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)

set -ex

cd "$SCRIPT_DIR/.."

if [ ! -d ./venv/ ]; then
    echo 'Missing python /venv/ dir.'
    exit 1
fi

./venv/bin/gunicorn 'src:app'
