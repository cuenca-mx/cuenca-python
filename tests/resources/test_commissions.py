import pytest

from cuenca import Commission


@pytest.mark.vcr
def test_commission_retrieve():
    id_commission = 'PAfj14vBZRaiq0Mo8JLToGw'
    commission: Commission = Commission.retrieve(id_commission)
    assert commission.id == id_commission
    assert not commission.related_transaction


@pytest.mark.vcr
def test_commission_retrieve_witw_cash_deposit():
    id_commission = 'PA7KR7uoZ7lsxG7cbyRqBJeh'
    commission: Commission = Commission.retrieve(id_commission)
    assert commission.id == id_commission
    related_transaction = commission.related_transaction
    assert related_transaction
    assert related_transaction.network == 'cash'


@pytest.mark.vcr
def test_commission_retrieve_witw_cash_transfer():
    id_commission = 'PA7KR7uoZ7lsxG7cbyRqBJeh'
    commission: Commission = Commission.retrieve(id_commission)
    assert commission.id == id_commission
    related_transaction = commission.related_transaction
    assert related_transaction
    assert related_transaction.network == 'spei'
