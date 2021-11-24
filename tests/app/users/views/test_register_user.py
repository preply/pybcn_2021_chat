import random
from fastapi.testclient import TestClient

from tests import faker

from app.config import API_PREFIX, AUTH_COOKIE_NAME
from app.users.constants import Lang


endpoint = f"{API_PREFIX}/users/register/"


def test_normal_flow(client: TestClient, user_factory) -> None:
    password = "some password"
    name = faker.name()

    r = client.post(
        endpoint,
        json={
            "password": password,
            "name": name,
            "lang": random.choice(list(Lang)).value,
        },
    )

    assert r.status_code == 200, f"body:{r.content}"
    assert r.cookies[AUTH_COOKIE_NAME]

    created_user = r.json()

    assert created_user["id"]
    assert created_user["name"] == name
    assert "password" not in created_user
