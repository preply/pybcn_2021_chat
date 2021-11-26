from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from lib.utils import get_random_uuid

from app.config import API_PREFIX
from app.rooms.models import Room


endpoint = f"{API_PREFIX}/rooms/%s/"


def test_normal_flow(client: TestClient, db: Session, room_factory) -> None:
    room = room_factory()
    room_id = room.id

    r = client.delete(endpoint % room_id)

    assert r.status_code == 200, f"body:{r.content}"
    deleted = r.json()

    assert deleted["id"] == room_id
    assert deleted["name"] == room.name

    db.expire_all()
    assert not db.query(Room).get(room_id)


def test_malformed_pk(
    client: TestClient,
    room_factory,
) -> None:
    room_factory()

    r = client.delete(endpoint % get_random_uuid())
    assert r.status_code == 404
