from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.common.schemas import InDBBase, ListBase
from app.users.constants import Lang


class UserRegister(BaseModel):
    name: str
    lang: Lang


class UserBase(BaseModel):
    name: str
    lang: Lang = Lang.EN


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(InDBBase, UserBase):
    updated_at: Optional[datetime]
    created_at: Optional[datetime]


class UsersList(ListBase):
    results: List[User]
