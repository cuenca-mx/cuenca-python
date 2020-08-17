import pytest
from cuenca_validations.types import TransactionStatus, TransferNetwork

from cuenca import WhatsappTransfer


@pytest.mark.vcr
def test_wa_transfer_cuenca():
    id_wa = 'SW01'
    wa_transfer: WhatsappTransfer = WhatsappTransfer.retrieve(id_wa)
    assert wa_transfer.id == id_wa
    assert wa_transfer.network == TransferNetwork.internal
    account = wa_transfer.destination
    assert account is not None
    assert account.id.startswith('LA')


@pytest.mark.vcr
def test_wa_transfer_spei():
    id_wa = 'SW03'
    wa_transfer: WhatsappTransfer = WhatsappTransfer.retrieve(id_wa)
    assert wa_transfer.id == id_wa
    assert wa_transfer.network == TransferNetwork.spei
    assert wa_transfer.destination_uri


@pytest.mark.vcr
def test_wa_transfer_submitted():
    id_wa = 'SW02'
    wa_transfer: WhatsappTransfer = WhatsappTransfer.retrieve(id_wa)
    assert wa_transfer.id == id_wa
    assert wa_transfer.status == TransactionStatus.submitted
    account = wa_transfer.destination
    assert account is None
