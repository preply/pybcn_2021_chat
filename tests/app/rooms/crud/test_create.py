import pytest
from sqlalchemy.orm import Session

from tests import faker

from app.common.crud import CRUDException
from app.rooms.crud import CRUD


def test_working_flow(db: Session):
    crud = CRUD(db)
    for i in range(5):
        data = {"name": faker.name()}
        item = crud.create(**data)

        db.refresh(item)
        assert item.id
        assert item.name == data["name"]
        assert item.created_at
        assert item.updated_at


def test_no_required_fields(db: Session):
    crud = CRUD(db)
    with pytest.raises(CRUDException):
        crud.create()
