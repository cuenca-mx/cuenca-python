import pytest
from cuenca_validations.types import Status
from pydantic import ValidationError

from cuenca import TerminalPayment
from cuenca.resources.terminal_payment import (  # TO-DO: cuenca_validations
    TerminalNetwork,
)


@pytest.mark.vcr
def test_create_terminal_payment():
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


def test_cannot_create_payment_without_required_attributes():
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


def test_cannot_create_payment_with_invalid_attributes():
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
