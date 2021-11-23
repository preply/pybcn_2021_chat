import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from lib.utils import get_random_uuid
from app.common.deps import get_current_user
from fastapi.testclient import TestClient

from app.config import AUTH_COOKIE_NAME


def test_normal_flow(client: TestClient, db: Session, login):
    admin = login()

    user = get_current_user(db=db, token=client.cookies[AUTH_COOKIE_NAME])
    assert user == admin


def test_no_user_failure(client: TestClient, db: Session, login):
    login()

    with pytest.raises(HTTPException):
        get_current_user(db=db, token=get_random_uuid())


def test_no_active_user_failure(client: TestClient, db: Session, login, user_factory):
    user = user_factory(is_active=False)
    login(user)

    with pytest.raises(HTTPException):
        get_current_user(db=db, token=client.cookies[AUTH_COOKIE_NAME])
