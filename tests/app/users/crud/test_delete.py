from sqlalchemy.orm import Session

from app.users.crud import UserCRUD
from app.users.models import User


def test_working_flow(db: Session, user_factory):
    user = user_factory()
    crud = UserCRUD(db)
    user_id = user.id

    assert db.query(User).get(user_id)

    result = crud.delete(user_id)

    assert result.id == user_id
    assert result.name == user.name

    db.expire_all()
    assert not db.query(User).get(user_id)
