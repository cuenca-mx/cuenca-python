import pytest

from cuenca import Account


@pytest.mark.vcr
def test_query_account(transfer):
    account: Account = Account.one(account_number=transfer.account_number)
    destination = transfer.destination
    assert account.id == destination.id
    assert account.account_number == destination.account_number
