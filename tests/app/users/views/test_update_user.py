import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests import faker

from app.config import API_PREFIX
from app.users.constants import Role, Lang

endpoint = f"{API_PREFIX}/users/%s/"


@pytest.mark.parametrize("role", Role)
@pytest.mark.parametrize("lang", Lang)
def test_normal_flow(
    client: TestClient, db: Session, user_factory, login, role, lang
) -> None:
    login()
    user = user_factory(role=Role.ADMIN)

    data = dict(
        role=role.value,
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
    assert str(user.role) == data["role"]
    assert str(user.lang) == data["lang"]


def test_not_superuser(
    client: TestClient,
    user_factory,
    login,
) -> None:
    user = user_factory(role=Role.USER)
    login(user)
    another = user_factory(role=Role.USER)

    data = dict(
        name=faker.name(),
        password=faker.phone_number(),
    )

    r = client.put(endpoint % another.id, json=data)

    assert r.status_code == 403
