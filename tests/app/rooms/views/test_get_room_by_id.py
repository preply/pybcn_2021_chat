from fastapi.testclient import TestClient

from app.config import API_PREFIX
from app.rooms.utils import translate
from app.users.constants import Role


endpoint = f"{API_PREFIX}/rooms/%s"


def test_normal_flow(client: TestClient, room_factory, login, user_factory) -> None:
    user = user_factory(role=Role.USER)
    login(user)
    room = room_factory()

    r = client.get(endpoint % room.id)

    assert r.status_code == 200, f"body:{r.content}"
    resp = r.json()

    assert resp == {
        "id": room.id,
        "name": room.name,
        "messages": [
            {
                "id": m.id,
                "text": translate(text=m.text, from_lang=m.lang, to_lang=user.lang),
                "lang": str(m.lang),
                "user_id": m.user_id,
                "created_at": m.created_at.isoformat(),
            }
            for m in room.messages
        ],
    }
