import os
import logging
from datetime import datetime

from fastapi import FastAPI
from application.routers import api_data

# logging
LOGS_DIR = os.getenv("LOGS_DIR")
os.makedirs(LOGS_DIR, exist_ok=True)

file_name = str(datetime.now().strftime("%d_%m_%Y")) + ".log"
logging.basicConfig(
    filename=LOGS_DIR + file_name,
    level=logging.DEBUG,
    format="%(asctime)s | {%(pathname)s:%(lineno)d} | %(module)s | %(levelname)s | %(funcName)s | %(message)s",
)

app = FastAPI()


app.include_router(api_data.router, prefix="/v1", tags=["v1"])
