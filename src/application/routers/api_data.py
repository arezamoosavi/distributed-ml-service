import os, io, hashlib, uuid
import logging

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from application.utils.mysql_db import insert_json_data, get_data_if_exists
from application.utils.minio_connection import MinioClient


# logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | {%(pathname)s:%(lineno)d} | %(module)s | %(levelname)s | %(funcName)s | %(message)s",
)

try:
    minio_obj = MinioClient()
    minio_client = minio_obj.client()
    minio_client.make_bucket("dataset")
except Exception as e:
    logging.error(str(e))


router = APIRouter()


@router.post("/load_data/")
async def load_data(dataset: UploadFile = File(None),):
    read_file = await dataset.read()
    data_buffer = io.BytesIO(read_file)
    buffer_length = data_buffer.getbuffer().nbytes

    md5 = hashlib.md5()
    md5.update(read_file)
    hash_id = md5.hexdigest()

    json_data = get_data_if_exists({"field": "hash_id", "val": hash_id}, "dataset")
    if json_data:
        return JSONResponse(
            content={"info": "ok", "data_id": json_data["dataset_id"]}, status_code=200
        )

    # save obj to minio with token
    try:
        json_data = {"dataset_id": uuid.uuid4().hex, "hash_id": hash_id}
        minio_client.put_object(
            bucket_name="dataset",
            object_name=f'{json_data["dataset_id"]}.csv',
            data=data_buffer,
            length=buffer_length,
        )
        insert_json_data(json_data, "dataset")

    except Exception as e:
        return JSONResponse(content={"info": str(e)}, status_code=400)

    return JSONResponse(
        content={"info": "ok", "data_id": json_data["dataset_id"]}, status_code=200,
    )
