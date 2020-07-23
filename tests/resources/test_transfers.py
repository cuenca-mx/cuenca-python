import pytest
from cuenca_validations.types import TransactionStatus, TransferNetwork
from pydantic import ValidationError

from cuenca import Transfer
from cuenca.exc import MultipleResultsFound, NoResultFound
from cuenca.resources.transfers import TransferRequest


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
    assert transfer.status == TransactionStatus.submitted
    assert transfer.network == TransferNetwork.internal
    account = transfer.destination
    assert account is None
    # Some seconds later
    transfer.refresh()
    assert transfer.status == TransactionStatus.succeeded
    account = transfer.destination
    assert account is not None


@pytest.mark.vcr
def test_transfers_create_many():
    valid = [
        TransferRequest(
            account_number='646180157034181180',
            amount=10000,
            descriptor='Mi primer transferencia',
            recipient_name='Rogelio Lopez',
            idempotency_key='35b241e25814445faf25c9cbcfc388a6',
        ),
        TransferRequest(
            account_number='646180157034181180',
            amount=10001,
            descriptor='Mi segundo transferencia',
            recipient_name='Rogelio Lopez',
            idempotency_key='dc15fc432a734724ab1e5884a4a24a2c',
        ),
    ]
    invalid = [
        TransferRequest(
            # BIN doesn't belong to any MX banks
            account_number='4050000000000001',
            amount=10002,
            descriptor='Mi transferencia invalida',
            recipient_name='Rogelio Lopez',
            idempotency_key='4a92e77054ba4e369a134e400f7c313e',
        ),
    ]
    transfers = Transfer.create_many(valid + invalid)
    assert {req.idempotency_key for req in valid} == {
        tr.idempotency_key for tr in transfers['submitted']
    }
    assert all([tr.status == 'submitted' for tr in transfers['submitted']])
    assert len(transfers['errors']) == 1
    assert transfers['errors'][0]['request'] == invalid[0]
    # TODO (for Glen): add validation of the exception


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
        Transfer.one(status=TransactionStatus.submitted)


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
    transfers = Transfer.all(status=TransactionStatus.succeeded)
    assert all([tr.status is TransactionStatus.succeeded for tr in transfers])


@pytest.mark.vcr
def test_transfers_count():
    # Count all items
    count = Transfer.count()
    assert count == 42

    # Count with filters
    count = Transfer.count(status=TransactionStatus.succeeded)
    assert count == 4


@pytest.mark.vcr
def test_transfers_count_vs_all():
    assert Transfer.count(status=TransactionStatus.succeeded) == len(
        list(Transfer.all(status=TransactionStatus.succeeded))
    )
    assert Transfer.count() == len(list(Transfer.all()))


def test_invalid_params():
    with pytest.raises(ValidationError) as e:
        Transfer.one(invalid_param='invalid_param')
    assert 'extra fields not permitted' in str(e)
