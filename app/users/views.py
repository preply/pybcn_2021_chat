from typing import Any, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common import deps
from app.users import schemas
from app.users.crud import UserCRUD


router = APIRouter(prefix="/users")


@router.get("/", response_model=schemas.UsersList)
def read_users(
    page: Optional[int] = 1,
    query: Optional[str] = None,
    is_asc: Optional[bool] = True,
    sort_by: Optional[str] = "created_at",
    limit: Optional[int] = 100,
    db: Session = Depends(deps.get_db),
) -> Any:
    crud = UserCRUD(db)
    result = crud.get_multi(
        page=page,
        query=query,
        is_asc=is_asc,
        sort_by=sort_by,
        limit=limit,
    )
    return {"results": result, "total": result.query.count()}


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    data: schemas.UserCreate,
) -> Any:
    return UserCRUD(db).create(**data.dict())


@router.delete("/{user_id}/", response_model=schemas.User)
def delete_user(
    *,
    user_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    return UserCRUD(db).delete(user_id)


@router.post("/register/", response_model=schemas.User)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    data: schemas.UserRegister,
) -> Any:
    user = UserCRUD(db).create(**data.dict())
    return user


@router.get("/{user_id}/", response_model=schemas.User)
def read_user_by_id(
    user_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    return UserCRUD(db).get(user_id, silent=False)


@router.put("/{user_id}/", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    data: schemas.UserUpdate,
) -> Any:
    return UserCRUD(db).update(pk=user_id, **data.dict(exclude_unset=True))
