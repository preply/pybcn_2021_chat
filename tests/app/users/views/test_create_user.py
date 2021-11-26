from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests import faker

from app.config import API_PREFIX
from app.users.constants import Lang
from app.users.models import User


endpoint = f"{API_PREFIX}/users/"


def test_normal_flow(client: TestClient, db: Session) -> None:
    data = {"name": faker.name(), "lang": Lang.ES.value, "password": faker.name()}

    r = client.post(endpoint, json=data)

    assert r.status_code == 200, f"body:{r.content}"
    created = r.json()

    assert created["id"]
    assert created["name"] == data["name"]
    assert created["lang"] == data["lang"]
    assert "password" not in created

    db.expire_all()
    assert db.query(User).get(created["id"])


def test_duplicate(client: TestClient, user_factory) -> None:
    name = faker.name()
    user_factory(name=name)

    r = client.post(endpoint, json={"name": name, "password": "some pass"})
    assert r.status_code == 400, f"body:{r.content}"
