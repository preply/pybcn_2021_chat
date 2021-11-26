from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import Enum

from lib.db import Base
from lib.db.mixins import Dated
from lib.utils import get_random_uuid

from app.users.constants import Lang


class User(Base, Dated):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=False), primary_key=True, default=get_random_uuid, index=True
    )
    name = Column(String(256))
    lang = Column(Enum(Lang), default=Lang.EN)
