import pytest

from cuenca import Deposit


@pytest.mark.vcr
def test_deposit_retrieve():
    id_deposit = 'SP01'
    deposit: Deposit = Deposit.retrieve(id_deposit)
    assert deposit.id == id_deposit
    account = deposit.source
    assert account is not None
