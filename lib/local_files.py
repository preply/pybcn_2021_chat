import os
from typing import IO

from loguru import logger


def save_file_locally(folder: str, file_name: str, file: IO[bytes]) -> str:
    if not os.path.isdir(folder):
        os.makedirs(folder)
    path = os.path.join(folder, file_name)

    with open(path, "wb+") as f:
        f.write(file.read())
    logger.debug("Saved file:{name} to folder:{path}", name=file_name, path=path)
    return f"/{path}"


def delete_local_file(path: str) -> None:
    os.remove(path)
    logger.debug("Removed file:{path}", path=path)
