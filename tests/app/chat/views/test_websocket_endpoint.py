import pytest
from async_asgi_testclient import TestClient

from app.config import API_PREFIX
from tests import faker


endpoint = f"{API_PREFIX}/chat/ws/%s"


@pytest.mark.asyncio
async def test_normal_flow(client: TestClient, login, room_factory) -> None:
    """
    I still did not find howto test this endpoint properly
    """
    user = login()
    room = room_factory()
    message = faker.pystr(min_chars=10, max_chars=1024)

    websocket = client.websocket_connect(endpoint % room.id)
    await websocket.connect()
    resp = await websocket.receive_text()
    await websocket.send_text(message)
    assert resp == f"User #{user.name}: {message}"
    websocket.close()

