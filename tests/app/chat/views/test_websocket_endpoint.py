from threading import Thread

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

    received_msgs = []
    async with client.websocket_connect(endpoint % room.id) as websocket:

        async def observer():
            received_msgs.append(await websocket.receive_text())

        observer_thread = Thread(target=observer)
        observer_thread.start()

        await websocket.send_text(message)
        assert len(received_msgs) == 1
        assert received_msgs[0] == f"User #{user.name}: {message}"
