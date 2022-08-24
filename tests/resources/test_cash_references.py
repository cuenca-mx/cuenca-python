import pytest

from cuenca import CashReference


@pytest.mark.vcr
def test_cash_reference_retrieve():
    reference = 'CR4EI4kVBwHboi8gCUxMnP9q'
    clabe = CashReference.retrieve(reference)
    assert clabe
    assert clabe.id == reference
    assert clabe.number


@pytest.mark.vcr
def test_cash_reference_all():
    references = list(CashReference.all())
    assert len(references) == 1
