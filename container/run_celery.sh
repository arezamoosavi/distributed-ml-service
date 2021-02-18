#!/bin/sh


set -o errexit
set -o nounset


celery worker --app=application.celery_app.app:app -lINFO --concurrency=1 -Ofair --pool=eventlet --hostname=worker_1.kyc@%h


exec "$@"
