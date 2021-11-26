from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from lib.db import session
from lib.db.utils import create_tables, truncate_all_tables, create_db, drop_db
from app.run import app
from app.config import SQLALCHEMY_DATABASE_URI


pytest_plugins = [
    "tests.factories",
]


@pytest.fixture(scope="module")
def application() -> Generator[FastAPI, None, None]:
    yield app


@pytest.fixture(scope="module")
def client(application) -> Generator[TestClient, None, None]:
    with TestClient(application) as c:
        yield c


@pytest.fixture(autouse=True, scope="session")
def init_database(request):
    if not request.node.get_closest_marker("no_db"):
        drop_db(SQLALCHEMY_DATABASE_URI)
        create_db(SQLALCHEMY_DATABASE_URI)
        create_tables()
    yield


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    truncate_all_tables()
    db = session()
    try:
        yield db
    finally:
        db.close()
