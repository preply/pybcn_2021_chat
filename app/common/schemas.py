from typing import List, Any

from pydantic import BaseModel


class InDBBase(BaseModel):
    id: str = None

    class Config:
        orm_mode = True


class ListBase(BaseModel):
    results: List[Any]
    total: int
