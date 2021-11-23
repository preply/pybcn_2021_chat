from sqlalchemy import Column, Boolean, String, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import Enum

from lib.db import Base
from lib.db.mixins import Dated
from lib.utils import get_random_uuid

from app.config import SECRET_KEY
from app.users.constants import Role, Lang
from app.users.utils import hash_password


class User(Base, Dated):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=False), primary_key=True, default=get_random_uuid, index=True
    )
    name = Column(String(256), index=True, unique=True)
    password = Column(String(256), nullable=False)
    is_active = Column(Boolean(), default=True, index=True)
    role = Column(Enum(Role), default=Role.USER, index=True)
    lang = Column(Enum(Lang), default=Lang.EN, index=True)


@event.listens_for(User, "before_insert")
@event.listens_for(User, "before_update")
def hash_user_password(mapper, connect, target):
    if target.password:
        target.password = hash_password(salt=SECRET_KEY, password=target.password)
