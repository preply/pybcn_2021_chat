import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests import faker

from app.config import API_PREFIX
from app.users.constants import Lang


endpoint = f"{API_PREFIX}/users/%s/"


@pytest.mark.parametrize("lang", Lang)
def test_normal_flow(client: TestClient, db: Session, user_factory, lang) -> None:
    user = user_factory()

    data = dict(
        lang=lang.value,
        name=faker.name(),
        password=faker.phone_number(),
    )

    r = client.put(endpoint % user.id, json=data)

    assert r.status_code == 200, f"body:{r.content}"
    updated = r.json()

    assert updated["id"]
    assert updated["name"] == data["name"]
    assert "password" not in updated

    db.refresh(user)
    assert user.name == data["name"]
    assert user.lang.value == data["lang"]
