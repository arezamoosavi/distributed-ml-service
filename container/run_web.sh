#!/bin/sh


set -o errexit
set -o nounset

# jupyter lab --port=${API_PORT} --no-browser --ip=0.0.0.0 --allow-root

uvicorn application.run_api:app --host ${HOST} --port ${API_PORT} --reload --ws 'auto' --loop 'auto' --workers 4

exec "$@"
