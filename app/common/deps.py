from typing import Generator

from fastapi import Depends, HTTPException, status, WebSocket
from fastapi.security import APIKeyCookie
from sqlalchemy.orm import Session

from lib.db import session

from app.config import AUTH_COOKIE_NAME
from app.common.auth.utils import get_user_id
from app.users.models import User
from app.users.constants import Role
from app.users.crud import UserCRUD


def get_db() -> Generator[Session, None, None]:
    try:
        db = session()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(APIKeyCookie(name=AUTH_COOKIE_NAME)),
) -> User:
    user = None
    user_id = get_user_id(token)
    if user_id:
        user = UserCRUD(db).get(user_id)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return user


def get_websocket_user(
    websocket: WebSocket,
    db: Session = Depends(get_db),
) -> User:
    token = websocket.cookies.get(AUTH_COOKIE_NAME)
    user_id = get_user_id(token)
    user = UserCRUD(db).get(user_id) if user_id else None
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please log in first",
        )
    return user


def get_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not (current_user.is_active and current_user.role == Role.ADMIN):
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user
