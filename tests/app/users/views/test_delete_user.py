from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from lib.utils import get_random_uuid

from app.config import API_PREFIX
from app.users.models import User


endpoint = f"{API_PREFIX}/users/%s/"


def test_normal_flow(client: TestClient, db: Session, user_factory) -> None:
    user = user_factory()
    user_id = user.id

    r = client.delete(endpoint % user_id)

    assert r.status_code == 200, f"body:{r.content}"
    deleted = r.json()

    assert deleted["id"] == user_id
    assert deleted["name"] == user.name

    db.expire_all()
    assert not db.query(User).get(user_id)


def test_malformed_pk(
    client: TestClient,
    user_factory,
) -> None:
    user_factory()

    r = client.delete(endpoint % get_random_uuid())
    assert r.status_code == 404
