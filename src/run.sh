#!/bin/sh


set -o errexit
set -o nounset


celery worker --app=celery_app.app:app -lINFO --concurrency=1 -Ofair --pool=eventlet --hostname=worker@%h | \
uvicorn run_api:app --host "0.0.0.0" --port $PORT --reload --ws 'auto' --loop 'auto' --workers 1

exec "$@"
