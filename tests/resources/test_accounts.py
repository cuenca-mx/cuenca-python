import pytest

from cuenca.resources import Account, Transfer


@pytest.mark.vcr
def test_query_account(transfer: Transfer):
    account = Account.one(account_number=transfer.account_number)
    assert account.account_number == transfer.destination.account_number
