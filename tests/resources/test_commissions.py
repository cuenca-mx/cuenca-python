import pytest

from cuenca import Commission, Deposit, Transfer


@pytest.mark.vcr
def test_commission_retrieve():
    id_commission = 'COXXX'
    commission: Commission = Commission.retrieve(id_commission)
    assert commission.id == id_commission


@pytest.mark.vcr
def test_commission_retrieve_with_cash_deposit():
    id_commission = 'COXXX'
    commission: Commission = Commission.retrieve(id_commission)
    assert commission.id == id_commission
    related_transaction = commission.related_transaction
    assert related_transaction
    assert type(related_transaction) == Deposit
    assert related_transaction.network == 'cash'


@pytest.mark.vcr
def test_commission_retrieve_with_cash_transfer():
    id_commission = 'COXXX'
    commission: Commission = Commission.retrieve(id_commission)
    assert commission.id == id_commission
    related_transaction = commission.related_transaction
    assert related_transaction
    assert type(related_transaction) == Transfer
    assert related_transaction.network == 'spei'
