from itertools import repeat

from fastapi.testclient import TestClient

from app.config import API_PREFIX
from app.users.constants import Role


endpoint = f"{API_PREFIX}/rooms/"


def test_normal_flow(client: TestClient, room_factory, login) -> None:
    login()

    # some noise
    [f() for f in list(repeat(room_factory, 5))]

    r = client.get(endpoint, params={"limit": 3})

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

    r = client.get(endpoint)
    assert r.status_code == 403
