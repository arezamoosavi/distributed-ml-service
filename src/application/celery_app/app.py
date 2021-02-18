from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

basedir = os.path.dirname(os.path.realpath(__file__))
BROKER_URL = os.environ.get("RMQ_URL", "amqp://admin:mypass@rabbitmq:5672")

app = Celery(
    "ml_app",
    broker=BROKER_URL,
    backend="db+sqlite:///" + os.path.join(basedir, "celery_results.db"),
    include=["application.celery_app.tasks",],
)

app.conf["task_acks_late"] = True
app.conf["worker_prefetch_multiplier"] = 1
