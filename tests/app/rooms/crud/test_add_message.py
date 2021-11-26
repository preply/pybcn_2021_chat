from sqlalchemy.orm import Session

from tests import faker

from app.rooms.crud import RoomCRUD


def test_working_flow(db: Session, room_factory, user_factory):
    crud = RoomCRUD(db)
    user = user_factory()
    room = room_factory()
    messages_len = len(room.messages)

    data = {"text": faker.name()}
    msg = crud.add_message(room_id=room.id, user_id=user.id, lang=user.lang, **data)

    db.refresh(room)
    assert msg.room_id == room.id
    assert msg.user_id == user.id
    assert msg.lang == user.lang
    assert len(room.messages) == messages_len + 1
    assert msg.text == data["text"]
    assert msg.user == user
    assert room.messages[-1].id == msg.id
