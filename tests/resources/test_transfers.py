import pytest
from pydantic import ValidationError

from cuenca import Transfer
from cuenca.exc import MultipleResultsFound, NoResultFound
from cuenca.types import Network, Status


@pytest.mark.vcr
def test_transfers_create():
    transfer = Transfer.create(
        account_number='646180157034181180',
        amount=10000,
        descriptor='Mi primer transferencia',
        recipient_name='Rogelio Lopez',
    )
    assert transfer.id is not None
    assert transfer.idempotency_key is not None
    assert transfer.status
    assert transfer.status == Status.created
    # Some seconds latter
    transfer.refresh()
    assert transfer.status == Status.succeeded
    assert transfer.network == Network.internal


@pytest.mark.vcr
def test_transfers_retrieve():
    id_transfer = 'test'
    transfer: Transfer = Transfer.retrieve(id_transfer)
    assert transfer.id == id_transfer
    assert transfer.status is not None


@pytest.mark.vcr
def test_transfers_one():
    key = 'idempotency_key_1'
    transfer: Transfer = Transfer.one(idempotency_key=key)
    assert transfer.idempotency_key == key


@pytest.mark.vcr
def test_transfers_one_errors():
    with pytest.raises(NoResultFound):
        Transfer.one(idempotency_key='wrong_key')

    with pytest.raises(MultipleResultsFound):
        Transfer.one(status=Status.created)


@pytest.mark.vcr
def test_transfers_first():
    account = '646180157013244941'
    transfer = Transfer.first(account_number=account)
    assert transfer is not None
    assert transfer.account_number == account
    transfer = Transfer.first(account_number='bad_account')
    assert transfer is None


@pytest.mark.vcr
def test_transfers_all():
    transfers = Transfer.all(status=Status.succeeded)
    assert all([tr.status is Status.succeeded for tr in transfers])


@pytest.mark.vcr
def test_transfers_count():
    # Count all items
    count = Transfer.count()
    assert count == 42

    # Count with filters
    count = Transfer.count(status=Status.succeeded)
    assert count == 4


@pytest.mark.vcr
def test_transfers_count_vs_all():
    assert Transfer.count(status=Status.succeeded) == len(
        list(Transfer.all(status=Status.succeeded))
    )
    assert Transfer.count() == len(list(Transfer.all()))


def test_invalid_params():
    with pytest.raises(ValidationError) as e:
        Transfer.one(invalid_param='invalid_param')
    assert 'extra fields not permitted' in str(e)
