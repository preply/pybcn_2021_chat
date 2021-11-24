from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from lib.utils import get_random_uuid

from app.config import API_PREFIX
from app.users.constants import Role
from app.users.models import User


endpoint = f"{API_PREFIX}/users/%s/"


def test_normal_flow(client: TestClient, db: Session, user_factory, login) -> None:
    login()
    user = user_factory(role=Role.USER)
    user_id = user.id

    r = client.delete(endpoint % user_id)

    assert r.status_code == 200, f"body:{r.content}"
    deleted = r.json()

    assert deleted["id"] == user_id
    assert deleted["name"] == user.name

    db.expire_all()
    assert not db.query(User).get(user_id)


def test_deleting_yourself(client: TestClient, db: Session, user_factory, login) -> None:
    user = login()

    r = client.delete(endpoint % user.id)

    assert r.status_code == 400, f"body:{r.content}"

    db.expire_all()
    assert db.query(User).get(user.id)


def test_not_superuser(
    client: TestClient,
    user_factory,
    login,
) -> None:
    user = user_factory(role=Role.USER)
    login(user)
    another_user = user_factory(role=Role.USER)

    r = client.delete(endpoint % another_user.id)
    assert r.status_code == 403


def test_malformed_pk(
    client: TestClient,
    user_factory,
    login,
) -> None:
    admin = user_factory(role=Role.ADMIN)
    login(admin)
    user_factory(role=Role.USER)

    r = client.delete(endpoint % get_random_uuid())
    assert r.status_code == 404
