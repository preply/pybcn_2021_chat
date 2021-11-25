from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Text,
)
from sqlalchemy.types import Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from lib.db import Base
from lib.db.mixins import Dated
from lib.utils import get_random_uuid

from app.users.constants import Lang
from app.users.models import User


class Message(Base, Dated):
    __tablename__ = "messages"

    id = Column(
        UUID(as_uuid=False), primary_key=True, default=get_random_uuid, index=True
    )
    room_id = Column(
        UUID(as_uuid=False),
        ForeignKey("rooms.id", ondelete="CASCADE"),
    )
    user_id = Column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    text = Column(Text, nullable=False)
    lang = Column(Enum(Lang), nullable=False)
    user = relationship(User, lazy="joined", uselist=False)


class Room(Base, Dated):
    __tablename__ = "rooms"

    id = Column(
        UUID(as_uuid=False), primary_key=True, default=get_random_uuid, index=True
    )

    name = Column(String(256), nullable=False, index=True)
    messages = relationship(Message, lazy="joined", order_by=Message.created_at.asc())
