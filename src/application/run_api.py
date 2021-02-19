import os
import logging
from datetime import datetime

from fastapi import FastAPI
from application.routers import api_data, api_model

app = FastAPI()

app.include_router(api_data.router, prefix="/v1", tags=["data"])
app.include_router(api_model.router, prefix="/v1", tags=["model"])
