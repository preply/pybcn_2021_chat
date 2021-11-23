import pytest

from app.common.auth.utils import AUTH_KEY


@pytest.mark.parametrize("token", [123, "123", 0, "some string", "#$%^&*"])
def test_working_flow(token):
    res = AUTH_KEY % token
    assert isinstance(res, str)
    assert res.endswith(str(token))
