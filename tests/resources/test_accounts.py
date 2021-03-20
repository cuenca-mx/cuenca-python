import pytest

from cuenca.resources import Account, Transfer


@pytest.mark.vcr
def test_query_account(transfer: Transfer):
    destination = transfer.destination
    account = Account.one(account_number=transfer.account_number)
    assert account.id == destination.id
    assert account.account_number == destination.account_number
