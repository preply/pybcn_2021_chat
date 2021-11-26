from itertools import repeat

from fastapi.testclient import TestClient

from app.config import API_PREFIX


endpoint = f"{API_PREFIX}/rooms/"


def test_normal_flow(client: TestClient, room_factory) -> None:
    [f() for f in list(repeat(room_factory, 5))]

    r = client.get(endpoint, params={"limit": 3})

    assert r.status_code == 200, f"body:{r.content}"
    data = r.json()
    assert set(data.keys()) == {"results", "total"}

    assert len(data["results"]) == 3
    assert data["total"] == 5
