from fastapi.testclient import TestClient

from app.config import API_PREFIX
from app.rooms.utils import translate
from app.users.constants import Role
from tests import faker

endpoint = f"{API_PREFIX}/rooms/%s/messages/"


def test_normal_flow(client: TestClient, room_factory, login, user_factory) -> None:
    user = user_factory(role=Role.USER)
    login(user)
    room = room_factory()

    text = faker.pystr(min_chars=10, max_chars=1024)

    r = client.post(endpoint % room.id, json={"text": text})

    assert r.status_code == 200, f"body:{r.content}"
    resp = r.json()

    assert set(resp.keys()) == {"id", "name", "messages"}
    assert resp["messages"][-1]["text"] == text
    assert resp["messages"][-1]["user_id"] == user.id
