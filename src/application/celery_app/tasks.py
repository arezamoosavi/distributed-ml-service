import io, os, time, json
import logging
from datetime import datetime

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


from celery import current_task
from .app import app as celery_app

from application.utils.mysql_db import update_json_data
from application.utils.minio_connection import MinioClient

# logging
LOGS_DIR = os.getenv("LOGS_DIR")
os.makedirs(LOGS_DIR, exist_ok=True)

file_name = str(datetime.now().strftime("%d_%m_%Y")) + ".log"
logging.basicConfig(
    filename=LOGS_DIR + file_name,
    level=logging.DEBUG,
    format="%(asctime)s | {%(pathname)s:%(lineno)d} | %(module)s | %(levelname)s | %(funcName)s | %(message)s",
)

try:
    minio_obj = MinioClient()
    minio_client = minio_obj.client()
except Exception as e:
    logging.error(str(e))


@celery_app.task(name="train_classifier")
def train_clf(data_json):

    # get csv data
    file_data = minio_client.get_object("dataset", data_json["dataset_id"])
    buffer_data = io.BytesIO(file_data.data)
    df = pd.read_csv(buffer_data)

    # select x y
    X = df[[col for col in data_json["feature_column"].split(",")]]
    y = df[data_json["class_column"]]

    # test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=data_json["test_ratio"], random_state=12345
    )

    # training

    tic = time.time()
    model = None
    try:
        if data_json["model_type"] == "logistic_regression":
            model = LogisticRegression()
            model.fit(X_train, y_train)
        elif data_json["model_type"] == "random_forest":
            model = RandomForestClassifier()
            model.fit(X_train, y_train)
            # model.fit(X_train, y_train.values.ravel())
    except Exception as e:
        logging.error(str(e))

    toc = time.time()
    duration = toc - tic

    # get test result
    if model:
        y_pred = model.predict(X_test)
        json_result = classification_report(y_test, y_pred, output_dict=True)
    else:
        json_result = "model is wrong"

    res_data = {
        "pk_field": "model_id",
        "model_id": current_task.request.id,
        "update_data": {"duration": duration, "result": json.dumps(json_result),},
    }

    # save to mysql
    try:
        update_json_data(res_data, "model_training")
    except Exception as e:
        logging.error(f"something went wrong: {str(e)}")

    return res_data["result"]
