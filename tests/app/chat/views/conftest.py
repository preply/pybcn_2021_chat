from typing import Generator

import pytest

from async_asgi_testclient import TestClient


@pytest.fixture
@pytest.mark.asyncio
async def client(application) -> Generator[TestClient, None, None]:
    async with TestClient(application) as c:
        yield c
