from app.common.auth.utils import get_user_id, AUTH_KEY
from lib.utils import get_random_uuid


def test_working_flow(redis):
    user_id = get_random_uuid()
    token = "some token"
    redis.set(name=AUTH_KEY % token, value=user_id)

    assert user_id == get_user_id(token)
