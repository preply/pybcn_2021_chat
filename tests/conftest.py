from typing import Generator

import pytest
from fastapi.testclient import TestClient
from redis import Redis
from sqlalchemy.orm import Session

from lib.db import session
from lib.db.utils import create_tables, truncate_all_tables, create_db, drop_db
from lib.factory import get_redis

from app.run import app
from app.config import AUTH_COOKIE_NAME, SQLALCHEMY_DATABASE_URI
from app.common.auth import utils as auth
from app.users.constants import Role
from app.users.models import User


pytest_plugins = [
    "tests.factories",
]


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
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


@pytest.fixture(scope="function", autouse=True)
def redis(mocker) -> Generator[Redis, None, None]:
    redis = get_redis()
    redis.flushall()

    mocker.patch("lib.factory.get_redis", return_value=redis)
    yield redis


@pytest.fixture
def login(client: TestClient, user_factory):
    def func(user: User = None) -> User:
        user = user or user_factory(role=Role.ADMIN)
        client.cookies[AUTH_COOKIE_NAME] = auth.set_user_id(user.id)
        return user

    return func
