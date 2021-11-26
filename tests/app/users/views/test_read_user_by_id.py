from fastapi.testclient import TestClient

from app.config import API_PREFIX
from lib.utils import get_random_uuid


endpoint = f"{API_PREFIX}/users/%s/"


def test_normal_flow(client: TestClient, user_factory) -> None:
    user = user_factory()

    r = client.get(endpoint % user.id)

    assert r.status_code == 200, f"body:{r.content}"
    data = r.json()

    assert data["id"] == user.id
    assert data["name"] == user.name
    assert data["created_at"]
    assert data["updated_at"]


def test_malformed_user_id(
    client: TestClient,
    user_factory,
) -> None:
    user_factory()

    r = client.get(endpoint % get_random_uuid())
    assert r.status_code == 404
