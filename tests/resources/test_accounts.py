import pytest

from cuenca.resources import Account


@pytest.mark.vcr
def test_account():
    account = Account.first(account_number='123456789')
    assert account.id == 'AC01'
    assert account.institution_name == 'Banamex'
