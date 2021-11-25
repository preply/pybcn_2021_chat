import pytest
from fastapi.testclient import TestClient

from app.config import API_PREFIX
from app.users.constants import Role


endpoint = f"{API_PREFIX}/users/me/"


@pytest.mark.parametrize("role", Role)
def test_normal_flow(client: TestClient, user_factory, login, role) -> None:
    user = user_factory(role=role)
    another_user = user_factory(role=role)
    login(user)

    r = client.get(endpoint)

    assert r.status_code == 200, f"body:{r.content}"
    current_user = r.json()

    assert current_user["id"] == user.id
    assert current_user["name"] == user.name

    login(another_user)

    r = client.get(endpoint)

    assert r.status_code == 200, f"body:{r.content}"
    current_user = r.json()

    assert current_user["id"] == another_user.id
    assert current_user["name"] == another_user.name


def test_not_auth(
    client: TestClient,
    user_factory,
) -> None:
    user_factory(role=Role.USER)

    r = client.get(endpoint)
    assert r.status_code == 403
