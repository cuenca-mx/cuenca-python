import pytest
from requests import HTTPError

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
        recipient_name='Rogelio Lopez',
        # idempotency_key='your_own_key',
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


@pytest.mark.vcr
@pytest.mark.usefixtures('test_client')
def test_transfers_all():
    all_transfers = Transfer.all(status=Status.succeeded.value)

    for transfer in all_transfers:
        assert transfer.status == Status.succeeded


@pytest.mark.vcr
@pytest.mark.usefixtures('test_client')
def test_transfers_count():
    # Count all items
    count = Transfer.count()
    assert count == 42

    # Count with filters
    count = Transfer.count(status=Status.succeeded)
    assert count == 4


@pytest.mark.vcr
def test_client_errors():
    with pytest.raises(ValueError):
        Transfer.one(invalid_param='invalid_param')

    with pytest.raises(HTTPError) as ex:
        Transfer.one()
    assert 'Unauthorized' in str(ex)
