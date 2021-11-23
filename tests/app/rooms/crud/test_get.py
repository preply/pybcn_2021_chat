from sqlalchemy.orm import Session

from lib.utils import get_random_uuid

from app.rooms.crud import CRUD


def test_working_flow(db: Session, room_factory):
    room = room_factory()
    another = room_factory()
    crud = CRUD(db)

    item = crud.get(room.id)
    assert item
    assert item.id == room.id
    assert item.name == room.name
    assert item.messages

    item = crud.get(another.id)
    assert item
    assert item.id == another.id
    assert item.name == another.name
    assert item.messages

    item = crud.get(get_random_uuid())
    assert not item
