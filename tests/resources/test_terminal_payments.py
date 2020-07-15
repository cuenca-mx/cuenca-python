import pytest
from cuenca_validations.types import Status
from pydantic import ValidationError

from cuenca import TerminalPayment
from cuenca.exc import MultipleResultsFound, NoResultFound
from cuenca.resources.terminal_payment import (  # TO-DO: cuenca_validations
    TerminalNetwork,
)


# Retrieving terminal payments
@pytest.mark.vcr
def test_terminal_payment_retrieve():
    id_payment: str = "test"
    payment: TerminalPayment = TerminalPayment.retrieve(id_payment)
    assert payment.id == id_payment
    assert payment.status == Status.succeeded
    assert payment.confirmation_code == "ABC123"
    assert payment.network == TerminalNetwork.spei


@pytest.mark.vcr
def test_terminal_payment_one():
    key: str = "idempotency_key_1"
    payment: TerminalPayment = TerminalPayment.one(idempotency_key=key)
    assert payment.idempotency_key == key


@pytest.mark.vcr
def test_terminal_payment_errors():
    with pytest.raises(NoResultFound):
        TerminalPayment.one(idempotency_key="wrong_key")

    with pytest.raises(MultipleResultsFound):
        TerminalPayment.one(status=Status.submitted)


@pytest.mark.vcr
def test_terminal_payment_first():
    payment: TerminalPayment = TerminalPayment.first(status=Status.submitted)
    assert payment is not None
    assert payment.status == Status.submitted
    payment = TerminalPayment.first(network=TerminalNetwork.internal)
    assert payment is None


@pytest.mark.vcr
def test_terminal_payment_all():
    payments = TerminalPayment.all(status=Status.submitted)
    assert all([py.status is Status.submitted for py in payments])


@pytest.mark.vcr
def test_terminal_payment_count():
    # Count all items
    count: int = TerminalPayment.count()
    assert count == 12

    # Count with filters
    count: int = TerminalPayment.count(status=Status.succeeded)
    assert count == 3


# Creating terminal payments


@pytest.mark.vcr
def test_terminal_payment_create():
    payment = TerminalPayment.create(
        amount=5000,
        descriptor="Orden de Tacos #12",
        destination_uri="/accounts/L050",
        network=TerminalNetwork.card,
        sender_name="Monica Gomez",
        phone_number="525500001111",
    )
    assert payment.id is not None
    assert payment.idempotency_key is not None
    assert payment.status == Status.submitted
    assert payment.network == TerminalNetwork.card
    assert payment.amount == 5000
    assert payment.platform_fees == 1000
    assert payment.sender_name == "Monica Gomez"
    assert payment.phone_number == "525500001111"
    assert payment.external_processor_reference == "cs_test_12345678"


def test_terminal_payment_cannot_create_without_required_attrs():
    valid_attrs = {
        "amount": 5000,
        "descriptor": "Orden de Tacos #12",
        "destination_uri": "/accounts/L050",
        "network": TerminalNetwork.cash,
        "sender_name": "Monica Gomez",
        "phone_number": "525500001111",
    }

    # All attributes are required
    for attr in valid_attrs.keys():
        payload = valid_attrs.copy()
        del payload[attr]
        with pytest.raises(TypeError) as e:
            TerminalPayment.create(**payload)
        assert f"missing 1 required positional argument: '{attr}'" in str(e)


def test_terminal_payment_cannot_create_with_invalid_attrs():
    valid_attrs = {
        "amount": 5000,
        "descriptor": "Orden de Tacos #12",
        "destination_uri": "/accounts/L050",
        "network": TerminalNetwork.cash,
        "sender_name": "Monica Gomez",
        "phone_number": "525500001111",
    }

    # Invalid amount
    with pytest.raises(ValidationError) as e:
        TerminalPayment.create(**{**valid_attrs, "amount": 10.50})
    assert "value is not a valid integer" in str(e)

    # Invalid network
    with pytest.raises(ValidationError) as e:
        TerminalPayment.create(**{**valid_attrs, "network": "visa"})
    assert "value is not a valid enumeration" in str(e)
