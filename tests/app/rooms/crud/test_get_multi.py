from itertools import repeat
from sqlalchemy.orm import Session

from tests import faker
from app.rooms.crud import CRUD


def test_working_flow(db: Session, room_factory):
    crud = CRUD(db)
    limit = 5
    prefix = "fghsdsd"

    # some noise
    [f() for f in list(repeat(room_factory, 5))]

    rooms = []
    for i in range(5):
        rooms += [
            room_factory(name=f"{i}{prefix}{faker.name()}"),
            room_factory(name=f"{i}{faker.name()}{prefix}"),
        ]

    for page in range(2):
        items = crud.get_multi(
            query=prefix, page=page + 1, limit=limit, sort_by="created_at", is_asc=True
        )
        assert items[0].id == rooms[page * limit].id
