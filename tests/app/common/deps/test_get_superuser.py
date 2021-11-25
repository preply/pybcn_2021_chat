import pytest
from fastapi import HTTPException, status

from app.common.deps import get_superuser
from app.users.constants import Role


def test_normal_flow(user_factory):
    user = user_factory(role=Role.ADMIN, is_active=True)
    resp = get_superuser(current_user=user)
    assert resp == user


def test_inactive_user_failure(user_factory):
    user = user_factory(role=Role.ADMIN, is_active=False)
    with pytest.raises(HTTPException) as e:
        get_superuser(current_user=user)
    assert e.value.status_code == status.HTTP_403_FORBIDDEN


def test_not_admin_failure(user_factory):
    user = user_factory(role=Role.USER, is_active=True)
    with pytest.raises(HTTPException) as e:
        get_superuser(current_user=user)
    assert e.value.status_code == status.HTTP_403_FORBIDDEN
