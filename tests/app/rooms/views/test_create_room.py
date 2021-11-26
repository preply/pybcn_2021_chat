from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests import faker

from app.config import API_PREFIX
from app.rooms.models import Room


endpoint = f"{API_PREFIX}/rooms/"


def test_normal_flow(client: TestClient, db: Session, room_factory) -> None:
    data = {"name": faker.name()}

    r = client.post(endpoint, json=data)

    assert r.status_code == 200, f"body:{r.content}"
    created = r.json()
    assert created["id"]
    assert created["name"] == data["name"]

    db.expire_all()
    assert db.query(Room).get(created["id"])
