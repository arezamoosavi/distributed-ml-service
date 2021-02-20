from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

basedir = os.path.dirname(os.path.realpath(__file__))

app = Celery(
    "ml_app",
    broker="sqla+sqlite:///" + os.path.join(basedir, "celery.db"),
    backend="db+sqlite:///" + os.path.join(basedir, "celery_results.db"),
    include=[
        "celery_app.tasks",
    ],
)

app.conf["task_acks_late"] = True
app.conf["worker_prefetch_multiplier"] = 1
