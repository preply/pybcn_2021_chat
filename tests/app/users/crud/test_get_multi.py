from itertools import repeat

from sqlalchemy.orm import Session

from app.users.constants import Role
from app.users.crud import UserCRUD


def test_working_flow(db: Session, user_factory):
    crud = UserCRUD(db)

    limit = 10
    prefix = "fghsdsd"

    # some noise
    [f() for f in list(repeat(user_factory, 5))]

    users = [user_factory(name=f"{i}{prefix}{i}") for i in range(10)]

    for page in range(2):
        items = crud.get_multi(
            query=prefix, page=page + 1, limit=limit, sort_by="created_at", is_asc=True
        )
        for i, item in enumerate(items):
            assert item.id == users[i + page * limit].id


def test_filters(db: Session, user_factory):
    crud = UserCRUD(db)

    u1 = user_factory(is_active=False, role=Role.USER)
    u2 = user_factory(is_active=True, role=Role.ADMIN)
    u3 = user_factory(is_active=False, role=Role.ADMIN)
    u4 = user_factory(is_active=True, role=Role.USER)

    items = crud.get_multi(is_active=False)
    assert {u1.id, u3.id} == {i.id for i in items}

    items = crud.get_multi(is_active=True)
    assert {u2.id, u4.id} == {i.id for i in items}

    items = crud.get_multi(role=Role.ADMIN)
    assert {u2.id, u3.id} == {i.id for i in items}
