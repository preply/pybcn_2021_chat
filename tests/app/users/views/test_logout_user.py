from fastapi.testclient import TestClient

from app.common.auth import utils as auth
from app.config import API_PREFIX, AUTH_COOKIE_NAME

endpoint = f"{API_PREFIX}/users/logout/"


def test_normal_flow(client: TestClient, login) -> None:
    login()
    token = client.cookies[AUTH_COOKIE_NAME]
    assert token
    assert auth.get_user_id(token)

    r = client.post(endpoint)

    assert r.status_code == 204, f"body:{r.content}"
    assert not auth.get_user_id(token)
