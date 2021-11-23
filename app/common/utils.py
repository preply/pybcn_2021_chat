import os
import uuid
from typing import IO

from app.config import UPLOAD_DIR, UPLOAD_BUCKET, ENV
from lib.local_files import save_file_locally
from lib.gcs import upload_blob


def save_image(file: IO[bytes], name: str) -> str:
    extension = name.split(".")[-1]
    return save_file(folder="images", file=file, ext=extension)


def save_file(folder: str, file: IO[bytes], ext: str, prefix: str = None) -> str:
    file_name = f'{prefix if prefix else ""}{uuid.uuid4()}.{ext}'

    if is_local():
        return save_file_locally(
            folder=os.path.join(UPLOAD_DIR, folder),
            file_name=file_name,
            file=file,
        )
    return upload_blob(
        bucket_name=UPLOAD_BUCKET,
        file=file,
        blob_name=os.path.join(folder, file_name),
    )


def is_local():
    return ENV == "local"
