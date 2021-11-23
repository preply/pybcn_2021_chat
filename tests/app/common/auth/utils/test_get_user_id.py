from lib.utils import get_random_uuid
from app.common.auth.utils import set_user_id, AUTH_KEY


def test_working_flow(redis):
    user_id = get_random_uuid()
    token = set_user_id(user_id)

    assert token and isinstance(token, str)
    assert user_id == redis.get(AUTH_KEY % token).decode()
