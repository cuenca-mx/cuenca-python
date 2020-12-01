import pytest

from cuenca.resources import BillPayment


@pytest.mark.vcr
def test_bill_payment():
    id_bill_payment = 'ST01'
    bill_payment = BillPayment.retrieve(id_bill_payment)
    assert bill_payment.id == id_bill_payment
    # It should always have a provider
    provider = bill_payment.provider
    assert provider is not None
