import pytest
from sqlalchemy.orm import Session

from lib.utils import get_random_uuid
from tests import faker

from app.common.crud import CRUDException
from app.users.crud import UserCRUD
from app.users.constants import Role, Lang


@pytest.mark.parametrize("role", Role)
@pytest.mark.parametrize("lang", Lang)
def test_working_flow(db: Session, user_factory, role, lang):
    crud = UserCRUD(db)
    user = user_factory()
    hashed_password = user.password
    updated_at = user.updated_at
    created_at = user.created_at

    data = dict(
        role=role,
        lang=lang,
        name=faker.name(),
        password=faker.phone_number(),
    )
    item = crud.update(pk=user.id, **data)
    db.refresh(item)

    assert item.id
    assert item.role == role
    assert item.lang == lang
    assert item.name == data["name"]

    # Check hashing
    assert item.password != hashed_password and item.password != data["password"]

    assert item.updated_at and item.updated_at != updated_at
    assert item.created_at == created_at


def test_duplicated(db: Session, user_factory):
    crud = UserCRUD(db)
    name = faker.name()
    user_factory(name=name)
    another_user = user_factory()

    with pytest.raises(CRUDException):
        crud.update(pk=another_user.id, name=name)


def test_no_user(db: Session, user_factory):
    crud = UserCRUD(db)
    user_factory()

    with pytest.raises(CRUDException):
        crud.update(pk=get_random_uuid(), role=Role.USER)
