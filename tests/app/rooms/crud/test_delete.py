from sqlalchemy.orm import Session

from app.rooms.crud import RoomCRUD


def test_working_flow(db: Session, room_factory):
    crud = RoomCRUD(db)
    room = room_factory()
    room_id = room.id

    result = crud.delete(room_id)

    assert result.id == room_id
    assert result.name == room.name

    db.expire_all()
    assert not crud.get(room_id)
