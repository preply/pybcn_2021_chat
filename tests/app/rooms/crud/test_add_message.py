from sqlalchemy.orm import Session

from tests import faker

from app.rooms.crud import RoomCRUD


def test_working_flow(db: Session, room_factory, user_factory):
    crud = RoomCRUD(db)
    user = user_factory()
    room = room_factory()
    messages_len = len(room.messages)

    data = {"text": faker.name()}
    item = crud.add_message(room_id=room.id, user_id=user.id, lang=user.lang, **data)

    assert item.id == room.id
    assert len(item.messages) == messages_len + 1
    assert item.messages[-1].text == data["text"]
    assert item.messages[-1].user_id == user.id
    assert item.messages[-1].lang == user.lang
