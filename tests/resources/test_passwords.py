import pytest

from cuenca import Password, UserLogin


@pytest.mark.vcr
def test_update_password():
    UserLogin.create('222222')
    Password.delete('222222')
    Password.create('111111')
