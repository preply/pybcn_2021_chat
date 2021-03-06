from datetime import datetime
from typing import List

from pydantic import BaseModel, constr

from app.common.schemas import InDBBase, ListBase
from app.users.constants import Lang


class RoomBase(BaseModel):
    name: constr(max_length=256)


class RoomCreate(RoomBase):
    pass


class Room(InDBBase, RoomBase):
    updated_at: datetime
    created_at: datetime


class RoomsList(ListBase):
    results: List[Room]


class User(InDBBase):
    id: str
    name: str


class Message(InDBBase):
    text: str
    lang: Lang
    created_at: datetime
    user: User


class RoomDetails(InDBBase, RoomBase):
    messages: List[Message]


class MessageCreate(BaseModel):
    text: str
