import pytest
from sqlalchemy.orm import Session

from tests import faker

from app.common.crud import CRUDException
from app.users.crud import UserCRUD
from app.users.constants import Lang


@pytest.mark.parametrize("lang", Lang)
def test_working_flow(db: Session, lang):
    crud = UserCRUD(db)
    data = dict(
        lang=lang,
        name=faker.name(),
    )

    item = crud.create(**data)
    db.refresh(item)
    assert item.id

    assert item.created_at
    assert item.updated_at


def test_default_values(db: Session):
    crud = UserCRUD(db)
    item = crud.create(
        name=faker.name(),
    )
    assert item.lang == Lang.EN
