import pytest
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from lib.utils import get_random_uuid
from app.config import AUTH_COOKIE_NAME
from app.common.deps import get_current_user


def test_normal_flow(client: TestClient, db: Session, login):
    admin = login()

    user = get_current_user(db=db, token=client.cookies[AUTH_COOKIE_NAME])
    assert user == admin


def test_no_user_failure(db: Session, login):
    login()

    with pytest.raises(HTTPException) as e:
        get_current_user(db=db, token=get_random_uuid())
    assert e.value.status_code == status.HTTP_403_FORBIDDEN


def test_no_active_user_failure(client: TestClient, db: Session, login, user_factory):
    user = user_factory(is_active=False)
    login(user)

    with pytest.raises(HTTPException) as e:
        get_current_user(db=db, token=client.cookies[AUTH_COOKIE_NAME])
    assert e.value.status_code == status.HTTP_403_FORBIDDEN
