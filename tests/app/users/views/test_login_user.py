from fastapi.testclient import TestClient

from app.config import API_PREFIX, AUTH_COOKIE_NAME


endpoint = f"{API_PREFIX}/users/login/"


def test_normal_flow(client: TestClient, user_factory) -> None:
    password = "some password"
    user = user_factory(password=password)

    r = client.post(
        endpoint,
        json={"password": password, "name": user.name},
    )

    assert r.status_code == 200, f"body:{r.content}"
    assert r.cookies[AUTH_COOKIE_NAME]

    created_user = r.json()

    assert created_user["id"]
    assert created_user["name"] == user.name
    assert "password" not in created_user


def test_wrong_credentials(client: TestClient, user_factory) -> None:
    password = "some password"
    user = user_factory(password=password)

    r = client.post(
        endpoint,
        json={"password": "wrong password", "name": user.name},
    )

    assert r.status_code == 403, f"body:{r.content}"
