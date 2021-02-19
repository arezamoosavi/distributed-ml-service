import os
from minio import Minio


class MinioClient:
    def __init__(self):

        self.minio_key = os.getenv("minio_key")
        self.minio_secret = os.getenv("minio_secret")
        self.minio_address = os.getenv("minio_address")

    def client(self):

        return Minio(
            self.minio_address,
            access_key=self.minio_key,
            secret_key=self.minio_secret,
            secure=False,
        )

