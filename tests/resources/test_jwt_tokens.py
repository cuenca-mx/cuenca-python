import pytest

from cuenca import JwtToken


@pytest.mark.vcr
def test_jwt_tokens():
    jwt_token = JwtToken.create()
    assert jwt_token
    assert isinstance(jwt_token.token, str)
