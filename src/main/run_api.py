from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import api_data, api_model

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
def root():
    return {"Hello to": "ML PIPELINE APP :)))", "GO to": "/docs or /redoc"}


app.include_router(api_data.router, prefix="/v1", tags=["data"])
app.include_router(api_model.router, prefix="/v1", tags=["model"])
