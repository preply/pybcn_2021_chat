from fastapi.testclient import TestClient

from app.config import API_PREFIX
from app.rooms.utils import translate


endpoint = f"{API_PREFIX}/rooms/%s/%s"


def test_normal_flow(client: TestClient, room_factory, user_factory) -> None:
    user = user_factory()
    room = room_factory()

    r = client.get(endpoint % (room.id, user.id))

    assert r.status_code == 200, f"body:{r.content}"
    resp = r.json()

    assert resp == {
        "id": room.id,
        "name": room.name,
        "messages": [
            {
                "id": m.id,
                "text": translate(text=m.text, from_lang=m.lang, to_lang=user.lang),
                "lang": m.lang.value,
                "created_at": m.created_at.isoformat(),
                "user": {
                    "id": m.user.id,
                    "name": m.user.name,
                },
            }
            for m in room.messages
        ],
    }
