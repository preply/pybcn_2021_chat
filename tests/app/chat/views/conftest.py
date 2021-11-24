from typing import Generator

import pytest

from async_asgi_testclient import TestClient

from app.common.auth import utils as auth
from app.config import AUTH_COOKIE_NAME
from app.users.constants import Role
from app.users.models import User


@pytest.fixture
@pytest.mark.asyncio
async def client(application) -> Generator[TestClient, None, None]:
    async with TestClient(application) as c:
        yield c


@pytest.fixture
def login(client: TestClient, user_factory):
    def func(user: User = None) -> User:
        user = user or user_factory(role=Role.ADMIN)
        client.cookie_jar[AUTH_COOKIE_NAME] = auth.set_user_id(user.id)
        return user

    return func
