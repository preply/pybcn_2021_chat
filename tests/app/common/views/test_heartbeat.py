import pytest
from fastapi.testclient import TestClient

from app.config import API_PREFIX


@pytest.mark.no_db
def test_create_item(client: TestClient):
    response = client.get(f"{API_PREFIX}/heartbeat/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
