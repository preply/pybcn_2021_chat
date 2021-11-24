from fastapi.testclient import TestClient

from app.config import API_PREFIX


endpoint = f"{API_PREFIX}/chat/"


def test_normal_flow(client: TestClient, login, room_factory) -> None:
    login()
    room_factory()

    r = client.get(endpoint)
    assert r.status_code == 200, f"body:{r.content}"
    assert r.template.name == 'index.html'
    assert "request" in r.context
