from typing import IO

from loguru import logger
from google.cloud import storage


def upload_blob(bucket_name: str, file: IO[bytes], blob_name: str) -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_file(file)
    logger.debug(
        "Uploaded file:{name} to folder:{path}", name=blob_name, path=bucket_name
    )
    return blob.public_url
