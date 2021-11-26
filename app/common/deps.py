from typing import Generator

from sqlalchemy.orm import Session

from lib.db import session


def get_db() -> Generator[Session, None, None]:
    try:
        db = session()
        yield db
    finally:
        db.close()
