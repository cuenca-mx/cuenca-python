import pytest
from cuenca_validations.types import BillPaymentRequest

from cuenca.resources import BillPayment


@pytest.mark.vcr
def test_bill_payment():
    id_bill_payment = 'ST01'
    bill_payment = BillPayment.retrieve(id_bill_payment)
    assert bill_payment.id == id_bill_payment
    # It should always have a provider
    provider = bill_payment.provider
    assert provider is not None


@pytest.mark.vcr
def test_create_bill_payment():
    bill_payment_request = BillPaymentRequest(
        account_number='000000000000000000000000000000',
        amount='1000',
        provider_id='SP01',
        field_type='barcode',
        user_id='US01',
    )
    bill_payment = BillPayment.create(**bill_payment_request.dict())
    assert bill_payment.id
    assert bill_payment.amount == bill_payment_request.amount
    assert bill_payment.account_number == bill_payment_request.account_number
    assert bill_payment.provider.id == bill_payment_request.provider_id
