#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

make collectstatic
make compress
make migrate
/usr/local/bin/gunicorn config.wsgi -w 4 -b 0.0.0.0:8080 --chdir=/app
