import pytest

from cuenca import Transfer
from cuenca.types import Status, Network


@pytest.mark.skip('oaxaca.sandbox is not ready')
@pytest.mark.usefixtures('test_client')
def test_api_keys_create():
    transfer = Transfer.create(
        account_number='646180157034181180',
        amount=10000,
        descriptor='Mi primer transferencia',
        receiver_name='Rogelio Lopez',
        idempotency_key='my_unique_id'
    )
    assert transfer.id is not None
    assert transfer.idempotency_key is not None
    assert transfer.status
    assert transfer.status == Status.pending
    # Some seconds latter
    transfer.refresh()
    assert transfer.status == Status.succeeded
    assert transfer.network == Network.internal
