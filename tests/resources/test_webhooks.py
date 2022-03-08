import pytest

from cuenca import Webhook


@pytest.mark.vcr
def test_webhook_retrieve():
    id_webhook = 'WE01'
    webhook: Webhook = Webhook.retrieve(id_webhook)
    assert webhook.id == id_webhook
    assert webhook.payload
    assert webhook.event


@pytest.mark.vcr
def test_webhook_all():
    assert list(Webhook.all())
