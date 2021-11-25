import pytest
from sqlalchemy.orm import Session

from lib.utils import get_random_uuid
from tests import faker

from app.common.crud import CRUDException
from app.rooms.crud import RoomCRUD


def test_working_flow(db: Session, room_factory):
    crud = RoomCRUD(db)

    room = room_factory()
    updated_at = room.updated_at
    created_at = room.created_at

    data = {"name": faker.name()}
    item = crud.update(pk=room.id, **data)

    assert item.id == room.id
    assert item.name == data["name"]
    assert item.updated_at and item.updated_at != updated_at
    assert item.created_at == created_at


def test_wrong_pk(db: Session, room_factory):
    crud = RoomCRUD(db)
    room_factory()

    with pytest.raises(CRUDException):
        crud.update(pk=get_random_uuid(), name="some name")
