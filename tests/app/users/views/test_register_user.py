import random
from fastapi.testclient import TestClient

from tests import faker

from app.config import API_PREFIX
from app.users.constants import Lang


endpoint = f"{API_PREFIX}/users/register/"


def test_normal_flow(client: TestClient, user_factory) -> None:
    name = faker.name()

    r = client.post(
        endpoint,
        json={
            "name": name,
            "lang": random.choice(list(Lang)).value,
        },
    )

    assert r.status_code == 200, f"body:{r.content}"
    created_user = r.json()
    assert created_user["id"]
    assert created_user["name"] == name
