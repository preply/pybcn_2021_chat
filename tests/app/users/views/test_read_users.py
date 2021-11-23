from fastapi.testclient import TestClient

from app.config import API_PREFIX
from app.users.constants import Role


endpoint = f"{API_PREFIX}/users/"


def test_normal_flow(client: TestClient, user_factory, login) -> None:
    login()

    for _ in range(5):
        user_factory(role=Role.USER)
    user_factory(role=Role.ADMIN)

    r = client.get(endpoint, params={"limit": 3, "role": Role.USER})

    assert r.status_code == 200, f"body:{r.content}"
    data = r.json()
    assert set(data.keys()) == {"results", "total"}

    assert len(data["results"]) == 3
    assert data["total"] == 5


def test_not_superuser(
    client: TestClient,
    user_factory,
    login,
) -> None:
    user = user_factory(role=Role.USER)
    login(user)
    user_factory()

    r = client.get(endpoint)

    assert r.status_code == 403
