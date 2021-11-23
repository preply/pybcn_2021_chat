from typing import Any, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common import deps
from app.users.models import User
from app.rooms import schemas
from app.rooms.crud import CRUD


router = APIRouter(prefix="/rooms")


@router.get("/", response_model=schemas.RoomsList)
def read_rooms(
    page: Optional[int] = 1,
    query: Optional[str] = None,
    user_id: Optional[str] = None,
    is_asc: Optional[bool] = True,
    sort_by: Optional[str] = "created_at",
    limit: Optional[int] = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_superuser),
) -> Any:
    crud = CRUD(db)
    result = crud.get_multi(
        page=page,
        query=query,
        user_id=user_id,
        is_asc=is_asc,
        sort_by=sort_by,
        limit=limit,
    )
    return {"results": result, "total": result.query.count()}


@router.post("/", response_model=schemas.Room)
def create_room(
    *,
    data: schemas.RoomCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_superuser),
) -> Any:
    crud = CRUD(db)

    return crud.create(**data.dict())


@router.get("/{room_id}/", response_model=schemas.RoomDetails)
def get_room_by_id(
    *,
    room_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    crud = CRUD(db)
    room = crud.get(room_id)
    room.messages = room.get_translated_messages(lang=current_user.lang)
    return room


@router.delete("/{room_id}/", response_model=schemas.Room)
def delete_room(
    *,
    room_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_superuser),
) -> Any:
    crud = CRUD(db)
    return crud.delete(room_id)


@router.post("/{room_id}/messages/", response_model=schemas.RoomDetails)
def post_message(
    *,
    room_id: str,
    data: schemas.MessageCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    crud = CRUD(db)
    room = crud.add_message(
        user_id=current_user.id, room_id=room_id, lang=current_user.lang, **data.dict()
    )
    room.messages = room.get_translated_messages(lang=current_user.lang)
    return room
