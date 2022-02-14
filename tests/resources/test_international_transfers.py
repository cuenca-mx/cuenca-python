from cuenca_validations.types import Country, TransactionStatus

import cuenca
from cuenca.cuenca_validations import Currency
from cuenca.resources import InternationalTransfer, Session


def test_international_transfers():
    # platform create an international transfer for user
    transfer = InternationalTransfer.create(
        user_id='USxxx',
        idempotency_key="MY_UNIQUE_KEY",
        bank_number="001287364",
        account_number="1024357689",
        account_country=Country.US,
        account_name="Amanda Brown",
        received_amount=20825,
        received_currency=Currency.mxn,
        sent_amount=1000,
        sent_currency=Currency.usd,
    )
    transfer_id = transfer.id
    assert transfer_id is not None
    assert transfer.idempotency_key is not None
    assert transfer.status == TransactionStatus.created

    # User has to confirm the transfer. Create a Session Token to allow it.
    session_token = Session.create('USxxx', 'session.transfers')
    user_session = cuenca.http.Session()
    user_session.configure(session_token=session_token.id)
    transfer = InternationalTransfer.update(
        transfer.id, status=TransactionStatus.submitted
    )
    assert transfer.id == transfer_id
    assert transfer.status == TransactionStatus.submitted

    # After SPEI deposit was received, status will change
    transfer.refresh()
    assert transfer.status == TransactionStatus.succeeded
