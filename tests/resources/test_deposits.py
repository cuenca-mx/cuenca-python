import pytest

from cuenca import Deposit


@pytest.mark.vcr
def test_deposit_retrieve_with_account():
    id_deposit = 'SP01'
    deposit: Deposit = Deposit.retrieve(id_deposit)
    assert deposit.id == id_deposit
    account = deposit.source
    assert account is not None


@pytest.mark.vcr
def test_deposit_retrieve_without_account():
    id_deposit = 'CD01'
    deposit: Deposit = Deposit.retrieve(id_deposit)
    assert deposit.id == id_deposit
    account = deposit.source
    assert account is None
