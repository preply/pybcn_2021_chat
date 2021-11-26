import pytest
from sqlalchemy.orm import Session

from app.config import SECRET_KEY
from app.users.utils import hash_password
from lib.utils import get_random_uuid
from tests import faker

from app.common.crud import CRUDException
from app.users.crud import UserCRUD
from app.users.constants import Lang


@pytest.mark.parametrize("lang", Lang)
def test_working_flow(db: Session, user_factory, lang):
    crud = UserCRUD(db)
    user = user_factory()
    hashed_password = user.password
    updated_at = user.updated_at
    created_at = user.created_at

    data = dict(
        lang=lang,
        name=faker.name(),
        password=faker.phone_number(),
    )
    item = crud.update(pk=user.id, **data)
    db.refresh(item)

    assert item.id
    assert item.lang == lang
    assert item.name == data["name"]

    # Check hashing
    assert (
        hashed_password
        != item.password
        == hash_password(salt=SECRET_KEY, password=data["password"])
    )

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
        crud.update(pk=get_random_uuid())
