from sqlalchemy.orm import Session

from app.rooms.crud import RoomCRUD
from app.rooms.models import Room


def test_working_flow(db: Session, room_factory):
    crud = RoomCRUD(db)
    assert db.query(Room).count() == 0

    first = crud.get_first_available_or_create()
    assert db.query(Room).count() == 1
    second = crud.get_first_available_or_create()
    assert first == second
