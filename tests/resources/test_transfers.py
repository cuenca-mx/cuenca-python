import pytest

from cuenca import Transfer
from cuenca.exc import MultipleResultsFound, NoResultFound
from cuenca.types import Network, Status


@pytest.mark.vcr
@pytest.mark.usefixtures('test_client')
def test_transfers_create():
    transfer = Transfer.create(
        account_number='646180157034181180',
        amount=10000,
        descriptor='Mi primer transferencia',
        receiver_name='Rogelio Lopez',
        idempotency_key='my_custom_id',
    )
    assert transfer.id is not None
    assert transfer.idempotency_key is not None
    assert transfer.status
    assert transfer.status == Status.pending
    # Some seconds latter
    transfer.refresh()
    assert transfer.status == Status.succeeded
    assert transfer.network == Network.internal


@pytest.mark.vcr
@pytest.mark.usefixtures('test_client')
def test_transfers_retrieve():
    id_transfer = 'TROIxvw5kJTBeYvEyuIe9Fgg=='
    transfer: Transfer = Transfer.retrieve(id_transfer)
    assert transfer.id == id_transfer
    assert transfer.status is not None


@pytest.mark.vcr
@pytest.mark.usefixtures('test_client')
def test_transfers_one():
    key = 'idempotency_key_1'
    transfer: Transfer = Transfer.one(idempotency_key=key)
    assert transfer.idempotency_key == key


@pytest.mark.vcr
@pytest.mark.usefixtures('test_client')
def test_transfers_one_errors():
    with pytest.raises(NoResultFound):
        Transfer.one(idempotency_key='wrong_key')

    with pytest.raises(MultipleResultsFound):
        Transfer.one(status=Status.pending)


@pytest.mark.vcr
@pytest.mark.usefixtures('test_client')
def test_transfers_first():
    account = '646180157013244941'
    transfer = Transfer.first(account_number=account)
    assert transfer is not None
    assert transfer.account_number == account
    transfer = Transfer.first(account_number='bad_account')
    assert transfer is None
