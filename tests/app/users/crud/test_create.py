import pytest
from sqlalchemy.orm import Session

from app.config import SECRET_KEY
from app.users.utils import hash_password
from tests import faker

from app.common.crud import CRUDException
from app.users.crud import UserCRUD
from app.users.constants import Role, Lang


@pytest.mark.parametrize("role", Role)
@pytest.mark.parametrize("lang", Lang)
def test_working_flow(db: Session, role, lang):
    crud = UserCRUD(db)
    data = dict(
        role=role,
        lang=lang,
        name=faker.name(),
        password="asddasdd",
    )

    item = crud.create(**data)
    db.refresh(item)
    assert item.id
    assert item.role == role

    # Check hashing
    assert item.password == hash_password(salt=SECRET_KEY, password=data["password"])

    assert item.created_at
    assert item.updated_at


def test_default_values(db: Session):
    crud = UserCRUD(db)
    item = crud.create(
        name=faker.name(),
        password="1212",
    )
    assert item.role == Role.USER
    assert item.lang == Lang.EN
    assert item.is_active


def test_no_required_fields(db: Session):
    crud = UserCRUD(db)
    with pytest.raises(CRUDException):
        crud.create(
            name=faker.name(),
        )


def test_duplicated_failure(db: Session):
    crud = UserCRUD(db)
    kwargs = {"name": faker.name(), "password": faker.name()}

    crud.create(**kwargs)

    kwargs["password"] = faker.name()
    with pytest.raises(CRUDException):
        crud.create(**kwargs)
