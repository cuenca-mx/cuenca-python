import pytest
from cuenca_validations.types import SessionType, TransactionStatus

import cuenca
from cuenca.exc import CuencaResponseException
from cuenca.resources import InternationalTransfer, Session


@pytest.mark.vcr
def test_create_international_transfer(international_transfer):
    transfer = InternationalTransfer.create(**international_transfer)
    transfer_id = transfer.id
    assert transfer_id is not None
    assert transfer.status == TransactionStatus.created

    # Create again with same data, return same transaction
    transfer = InternationalTransfer.create(**international_transfer)
    assert transfer.id == transfer_id

    # Duplicate your idempotency key with another data
    international_transfer['account_number'] = '9876543210'
    with pytest.raises(CuencaResponseException):
        InternationalTransfer.create(**international_transfer)


@pytest.mark.vcr
def test_retrieve_international_transfer():
    transfer_id = 'ITeGc6ZBb8S96zqDhtY0AO3g'
    transfer = InternationalTransfer.retrieve(transfer_id)
    assert transfer.id == transfer_id


@pytest.mark.vcr
def test_query_international_transfer():
    your_id = 'MY_UNIQUE_KEY'
    transfer = InternationalTransfer.one(idempotency_key=your_id)
    assert transfer.idempotency_key == your_id


@pytest.mark.vcr
def test_update_international_transfer():
    transfer_id = 'ITeGc6ZBb8S96zqDhtY0AO3g'
    # Cancel the transfer updating value to failed
    new_status = TransactionStatus.failed
    transfer = InternationalTransfer.update(transfer_id, new_status)
    assert transfer.id == transfer_id
    assert transfer.status == new_status


@pytest.mark.vcr
def test_complete_flow_international_transfers(international_transfer):
    # platform create an international transfer for user
    transfer = InternationalTransfer.create(**international_transfer)
    transfer_id = transfer.id
    assert transfer_id is not None
    assert transfer.status == TransactionStatus.created

    # Create a Session Token to allow user confirm or reject.
    user_id = international_transfer['user_id']
    session_token = Session.create(
        user_id, SessionType.international_transfers
    )

    # Using the session token, User has to confirm the transfer
    cuenca.configure(
        session_token=session_token.id, api_key=None, api_secret=None
    )
    transfer = InternationalTransfer.update(
        transfer.id, status=TransactionStatus.submitted
    )
    assert transfer.id == transfer_id
    assert transfer.status == TransactionStatus.submitted

    # After SPEI deposit was received, status will change
    transfer.refresh()
    assert transfer.status == TransactionStatus.succeeded
