import os
import logging
from datetime import datetime

from celery import current_task
from .app import app as celery_app

# logging
LOGS_DIR = os.getenv("LOGS_DIR")
os.makedirs(LOGS_DIR, exist_ok=True)

file_name = str(datetime.now().strftime("%d_%m_%Y")) + ".log"
logging.basicConfig(
    filename=LOGS_DIR + file_name,
    level=logging.DEBUG,
    format="%(asctime)s | {%(pathname)s:%(lineno)d} | %(module)s | %(levelname)s | %(funcName)s | %(message)s",
)


@celery_app.task(name="train_classifier")
def train_clf(data_json):
    results = {
        "data_id": None,
        "clf_column": None,
        "model_id": None,
        "started": None,
        "finished": None,
    }

    results["started"] = datetime.now().isoformat()
    results["model_id"] = current_task.request.id

    results["finished"] = datetime.now().isoformat()

    return results
