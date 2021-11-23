from sqlalchemy.orm import Session

from app.users.crud import CRUD
from lib.utils import get_random_uuid


def test_working_flow(db: Session, user_factory):
    user = user_factory()
    crud = CRUD(db)

    item = crud.get(user.id)
    assert item
    assert item.id == user.id
    assert item.name == user.name

    item = crud.get(get_random_uuid())
    assert not item
