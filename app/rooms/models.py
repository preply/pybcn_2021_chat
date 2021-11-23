from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Text,
)
from sqlalchemy.types import Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.rooms.utils import translate
from app.users.constants import Lang
from lib.db import Base
from lib.db.mixins import Dated
from lib.utils import get_random_uuid


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
    lang = Column(Enum(Lang), nullable=False, index=True)


class Room(Base, Dated):
    __tablename__ = "rooms"

    id = Column(
        UUID(as_uuid=False), primary_key=True, default=get_random_uuid, index=True
    )

    name = Column(String(256), nullable=False, index=True)
    messages = relationship(Message, lazy="joined", order_by=Message.created_at.asc())

    def get_translated_messages(self, lang: Lang):
        resp = []
        for msg in self.messages:
            msg.text = translate(text=msg.text, from_lang=msg.lang, to_lang=lang)
            resp.append(msg)
        return resp
