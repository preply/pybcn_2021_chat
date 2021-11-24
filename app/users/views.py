from typing import Any, Optional

from fastapi import APIRouter, Response, Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from sqlalchemy.orm import Session

from app.config import AUTH_COOKIE_NAME
from app.common.auth import utils as auth
from app.common import deps
from app.users import schemas, models
from app.users.constants import Role
from app.users.crud import CRUD


router = APIRouter(prefix="/users")


@router.get("/", response_model=schemas.UsersList)
def read_users(
    page: Optional[int] = 1,
    query: Optional[str] = None,
    role: Optional[Role] = None,
    is_active: Optional[bool] = None,
    is_asc: Optional[bool] = True,
    sort_by: Optional[str] = "created_at",
    limit: Optional[int] = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_superuser),
) -> Any:
    crud = CRUD(db)
    result = crud.get_multi(
        page=page,
        query=query,
        role=role,
        is_active=is_active,
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
    current_user: models.User = Depends(deps.get_superuser),
) -> Any:
    crud = CRUD(db)
    return crud.create(**data.dict())


@router.delete("/{user_id}/", response_model=schemas.User)
def delete_user(
    *,
    user_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_superuser),
) -> Any:
    crud = CRUD(db)
    if current_user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Can not delete yourself",
        )
    return crud.delete(user_id)


@router.get("/me/", response_model=schemas.User)
def get_current_user(
    *,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    return current_user


@router.post("/login/", response_model=schemas.User)
def login_user(
    *,
    db: Session = Depends(deps.get_db),
    data: schemas.UserLogin,
    response: Response,
) -> Any:
    crud = CRUD(db)
    user = crud.get_by_cred(**data.dict())
    if not (user and user.is_active):
        raise HTTPException(
            status_code=403,
            detail="Can not authorize user",
        )
    response.set_cookie(key=AUTH_COOKIE_NAME, value=auth.set_user_id(user.id))
    return user


@router.post("/register/", response_model=schemas.User)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    data: schemas.UserRegister,
    response: Response,
) -> Any:
    crud = CRUD(db)
    user = crud.create(**data.dict())
    response.set_cookie(key=AUTH_COOKIE_NAME, value=auth.set_user_id(user.id))
    return user


@router.post("/logout/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def logout_user(
    *,
    token: str = Depends(APIKeyCookie(name=AUTH_COOKIE_NAME)),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    auth.remove_user_id(token)


@router.get("/{user_id}/", response_model=schemas.User)
def read_user_by_id(
    user_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_superuser),
) -> Any:
    crud = CRUD(db)
    return crud.get(user_id, silent=False)


@router.put("/{user_id}/", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    data: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_superuser),
) -> Any:
    crud = CRUD(db)
    return crud.update(pk=user_id, **data.dict(exclude_unset=True))
