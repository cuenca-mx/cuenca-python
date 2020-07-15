import pytest
from cuenca_validations.types import Status

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
