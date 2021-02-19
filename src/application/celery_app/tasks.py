import io, os, time, json
import logging
from datetime import datetime

import tempfile
import joblib

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
logging.basicConfig(
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
    try:
        file_data = minio_client.get_object("dataset", f'{data_json["dataset_id"]}.csv')
        buffer_data = io.BytesIO(file_data.data)
        df = pd.read_csv(buffer_data)
    except Exception as e:
        msg_result = "dataset_id is wrong"
        logging.error(msg_result + f": {str(e)}")
        res_data = {
            "pk_field": "model_id",
            "model_id": current_task.request.id,
            "update_data": {"finished": datetime.now(), "duration": 0, "result": msg_result, },
        }
        try:
            update_json_data(res_data, "model_training")
        except:
            pass
        return msg_result

    # select x y
    try:
        X = df[[col for col in data_json["feature_column"].split(",")]]
        y = df[data_json["class_column"]]

        # test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=data_json["test_ratio"], random_state=12345
        )
    except Exception as e:
        msg_result = "feature_column and class_column are wrong"
        logging.error(msg_result + f": {str(e)}")
        res_data = {
            "pk_field": "model_id",
            "model_id": current_task.request.id,
            "update_data": {"finished": datetime.now(), "duration": 0, "result": msg_result, },
        }
        try:
            update_json_data(res_data, "model_training")
        except:
            pass
        return msg_result

    # training with selecting models!
    tic = time.time()
    try:
        if data_json["model_type"] == "logistic_regression":
            model = LogisticRegression()
        elif data_json["model_type"] == "random_forest":
            model = RandomForestClassifier()
        else:
            raise Exception("model name not found!")

        model.fit(X_train, y_train)
    except Exception as e:

        msg_result = "model name not found!"
        logging.error(msg_result + f": {str(e)}")
        res_data = {
            "pk_field": "model_id",
            "model_id": current_task.request.id,
            "update_data": {"finished": datetime.now(), "duration": 0, "result": msg_result, },
        }
        try:
            update_json_data(res_data, "model_training")
        except:
            pass
        return msg_result

    toc = time.time()
    duration = toc - tic

    # get test result
    try:
        y_pred = model.predict(X_test)
        json_result = classification_report(y_test, y_pred, output_dict=True)
    except Exception as e:
        msg_result = "error when trying to predic test data!"
        logging.error(msg_result + f": {str(e)}")
        res_data = {
            "pk_field": "model_id",
            "model_id": current_task.request.id,
            "update_data": {"finished": datetime.now(), "duration": 0, "result": msg_result, },
        }
        try:
            update_json_data(res_data, "model_training")
        except:
            pass
        return msg_result

    res_data = {
        "pk_field": "model_id",
        "model_id": current_task.request.id,
        "update_data": {"finished": datetime.now(), "duration": duration, "result": json.dumps(json_result), },
    }

    # save to minio
    logging.info("Write to minio: ")
    with tempfile.TemporaryFile() as fp:
        joblib.dump(model, fp)
        fp.seek(0)
        _buffer = io.BytesIO(fp.read())
        _length = _buffer.getbuffer().nbytes
        minio_client.put_object(
            bucket_name="models",
            object_name=f"{res_data['model_id']}.joblib",
            data=_buffer,
            length=_length,
        )
    logging.info("Saved to minio: ")

    # save results to mysql
    try:
        update_json_data(res_data, "model_training")
    except Exception as e:
        logging.error(f"something went wrong during save to db: {str(e)}")

    json_result["duration"] = duration
    return json_result
