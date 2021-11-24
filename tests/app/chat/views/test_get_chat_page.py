import pytest
from async_asgi_testclient import TestClient

from app.config import API_PREFIX


endpoint = f"{API_PREFIX}/chat/"


@pytest.mark.asyncio
async def test_normal_flow(client: TestClient, login, room_factory) -> None:
    room_factory()
    login()

    resp = await client.get(endpoint)
    assert resp.status_code == 200, f"body:{resp.content}"
