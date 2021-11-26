from itertools import repeat

from sqlalchemy.orm import Session

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
