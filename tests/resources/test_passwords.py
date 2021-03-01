import pytest

from cuenca import Password, UserLogin


@pytest.mark.vcr
def test_update_password():
    UserLogin.create('111111')
    Password.delete('111111')
    Password.create('222222')
