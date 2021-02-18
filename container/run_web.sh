#!/bin/sh


set -o errexit
set -o nounset

jupyter lab --port=${API_PORT} NotebookApp.token = '123' --no-browser --ip=0.0.0.0 --allow-root

# uvicorn run_api:app --host ${HOST} --port ${API_PORT} --reload --ws 'auto' --loop 'auto' --workers 4

exec "$@"
