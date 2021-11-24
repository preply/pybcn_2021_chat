from fastapi.testclient import TestClient

from app.config import API_PREFIX
from tests import faker


endpoint = f"{API_PREFIX}/chat/ws/%s/"


def test_normal_flow(client: TestClient, login, room_factory) -> None:
    user = login()
    room = room_factory()
    message = faker.pystr(min_chars=10, max_chars=1024)

    # TODO: this test fails =(
    with client.websocket_connect(endpoint % room.id) as websocket:
        websocket.send_text(message)
        resp = websocket.receive_text()
        assert resp == f"User #{user.name}: {message}"
        websocket.close()
