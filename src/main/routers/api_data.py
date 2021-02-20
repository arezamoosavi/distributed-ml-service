import os, io, hashlib, uuid
import logging
import pandas as pd

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from utils.mysql_db import insert_json_data, get_data_if_exists


# logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | {%(pathname)s:%(lineno)d} | %(module)s | %(levelname)s | %(funcName)s | %(message)s",
)

router = APIRouter()


@router.post("/load_data/")
async def load_data(dataset: UploadFile = File(None),):
    read_file = await dataset.read()
    data_buffer = io.BytesIO(read_file)

    md5 = hashlib.md5()
    md5.update(read_file)
    hash_id = md5.hexdigest()

    json_data = get_data_if_exists({"pk_field": "hash_id", "pk_val": hash_id}, "dataset")
    if json_data:
        return JSONResponse(
            content={"info": "ok", "data_id": json_data["dataset_id"]}, status_code=200
        )

    # save obj to dir with token
    try:
        json_data = {"dataset_id": uuid.uuid4().hex, "hash_id": hash_id}
        df = pd.read_csv(data_buffer)
        file_path = os.path.join(os.getcwd(), "storage", f'{json_data["dataset_id"]}.csv')
        df.to_csv(file_path, index=False)

        insert_json_data(json_data, "dataset")

    except Exception as e:
        return JSONResponse(content={"info": str(e)}, status_code=400)

    return JSONResponse(
        content={"info": "ok", "data_id": json_data["dataset_id"]}, status_code=200,
    )
