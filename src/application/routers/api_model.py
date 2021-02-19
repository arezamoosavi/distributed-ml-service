import os, io, uuid
import logging

import tempfile
import joblib

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse

from pydantic import BaseModel
from celery.result import AsyncResult

from application.utils.mysql_db import insert_json_data
from application.utils.minio_connection import MinioClient
from application.celery_app.tasks import train_clf

# logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | {%(pathname)s:%(lineno)d} | %(module)s | %(levelname)s | %(funcName)s | %(message)s",
)

try:
    minio_obj = MinioClient()
    minio_client = minio_obj.client()
    minio_client.make_bucket("models")
except Exception as e:
    logging.error(str(e))

router = APIRouter()


class TrainModel(BaseModel):
    dataset_id: str
    model_type: str
    class_column: str
    feature_column: str
    test_ratio: float


class ResultModel(BaseModel):
    model_id: str


@router.post("/train_model/")
async def train_model(data: TrainModel):
    """ Starts training model:

    Args:
        dataset_id: str :the csv data that has been loaded
        model_type: str :type of selected model
        class_column: str :Y column in data
        feature_column: str :X colums in data -> x1,x2,x3,x4: should be comma(,) seperated
        test_ratio: float   :test_size value between (0,1)

    Return
        A Json response for model_id that train is started!
    """
    try:
        json_data = data.dict()
        task_obj = train_clf.apply_async((json_data,), task_id=uuid.uuid4().hex)
        json_data["model_id"] = task_obj.id

        logging.info(f"task token {task_obj.id} is started!")

    except Exception as e:
        logging.error(f"something went wrong: {str(e)}")
        return JSONResponse(content={"info": "app_error"}, status_code=400)

    # save record to mysql
    try:
        insert_json_data(json_data, "model_training")
    except Exception as e:
        logging.error(f"something went wrong: {str(e)}")
        return JSONResponse(content={"info": "app_error"}, status_code=400)

    return JSONResponse(
        content={"info": "ok", "model_id": json_data["model_id"]}, status_code=200,
    )


@router.post("/model_result/")
async def model_result(data: ResultModel):
    model_id = data.model_id
    async_result = AsyncResult(model_id)
    if async_result.ready():
        res_status = "ready"
        res_data = async_result.result
    else:
        res_status = "pending"
        res_data = "null"

    return JSONResponse(
        content={"info": "ok", "status": res_status, "test_result": res_data},
        status_code=200,
    )


@router.post("/download_model/")
async def download_model(data: ResultModel):
    try:
        with tempfile.NamedTemporaryFile(mode="w+b", suffix=".joblib", delete=False) as tmp:
            minio_client.fget_object("models", f"{data.model_id}.joblib", tmp.name)

    except Exception as e:
        logging.error(f"something went wrong: {str(e)}")
        return JSONResponse(content={"info": "model not found"}, status_code=400)

    response = FileResponse(tmp.name,  status_code=200)
    response.headers["Content-Disposition"] = "attachment; filename={}.joblib".format(data.model_id)
    return response


@router.get("/model_types/")
async def model_types():
    return JSONResponse(
        content={"available_model_types": ["logistic_regression", "random_forest"]},
        status_code=200,
    )
