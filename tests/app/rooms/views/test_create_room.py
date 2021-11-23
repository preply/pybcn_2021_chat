from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests import faker

from app.config import API_PREFIX
from app.users.constants import Role
from app.rooms.models import Room


endpoint = f"{API_PREFIX}/rooms/"


def test_normal_flow(client: TestClient, db: Session, login, room_factory) -> None:
    login()
    data = {"name": faker.name()}

    r = client.post(endpoint, json=data)

    assert r.status_code == 200, f"body:{r.content}"
    created = r.json()
    assert created["id"]
    assert created["name"] == data["name"]

    db.expire_all()
    assert db.query(Room).get(created["id"])


def test_not_superuser(
    client: TestClient,
    user_factory,
    login,
) -> None:
    user = user_factory(role=Role.USER)
    login(user)

    r = client.post(endpoint, json={"name": faker.name()})
    assert r.status_code == 403
