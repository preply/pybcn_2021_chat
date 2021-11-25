from lib.utils import get_random_uuid

from app.common.auth.utils import remove_user_id, AUTH_KEY


def test_working_flow(redis):
    user_id = get_random_uuid()
    token = "some token"

    redis.set(name=AUTH_KEY % token, value=user_id)
    remove_user_id(token)

    assert not redis.get(AUTH_KEY % token)
