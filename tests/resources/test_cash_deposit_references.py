import pytest

from cuenca import CashDepositReference


@pytest.mark.vcr
def test_reference_retrieve():
    id_reference = 'CRXXX'
    reference = CashDepositReference.retrieve(id_reference)
    assert reference.id == id_reference


@pytest.mark.vcr
def test_query_my_reference():
    reference = CashDepositReference.one()
    assert reference.id is not None
    assert reference.partner == 'paynet'

