from fastapi.testclient import TestClient

from app.config import API_PREFIX
from app.users.constants import Role
from lib.utils import get_random_uuid


endpoint = f"{API_PREFIX}/users/%s/"


def test_normal_flow(client: TestClient, user_factory, login) -> None:
    login()
    user = user_factory(role=Role.USER)
    user_id = user.id

    r = client.get(endpoint % user_id)

    assert r.status_code == 200, f"body:{r.content}"
    data = r.json()

    assert data["id"] == user_id
    assert data["name"] == user.name
    assert data["created_at"]
    assert data["updated_at"]


def test_not_superuser(
    client: TestClient,
    user_factory,
    login,
) -> None:
    user = user_factory(role=Role.USER)
    login(user)
    another_user = user_factory(role=Role.USER)

    r = client.get(endpoint % another_user.id)
    assert r.status_code == 403


def test_malformed_user_id(
    client: TestClient,
    user_factory,
    login,
) -> None:
    login()
    user_factory(role=Role.USER)

    r = client.get(endpoint % get_random_uuid())
    assert r.status_code == 404
