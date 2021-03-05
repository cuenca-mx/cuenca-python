import pytest

from cuenca import CardTransaction


@pytest.mark.vcr
def test_card_transaction_parent_retrieve():
    ct = CardTransaction.retrieve('CT17YWLDHWI59r6F0oG1ihvK')
    related_cts = ct.related_card_transactions
    assert len(related_cts) == 2
    for card_transaction in related_cts:
        assert card_transaction.type != 'auth'


@pytest.mark.vcr
def test_card_transaction_child_retrieve():
    ct = CardTransaction.retrieve('CT4jC3Dh65FNmb0lGBTnvr4I')
    related_cts = ct.related_card_transactions
    assert len(related_cts) == 1
    assert related_cts[0].type == 'auth'


@pytest.mark.vcr
def test_card_transaction_refund_without_parent_id_retrieve():
    ct = CardTransaction.retrieve('CTKLh6VNCRTybvfpVSMLu8m')
    assert not ct.related_card_transactions


@pytest.mark.vcr
def test_card_transaction_expiration_retrieve():
    ct = CardTransaction.retrieve('CT4kMz2YNoWxVSQOCPCh2nQD')
    assert ct.type == 'expiration'


@pytest.mark.vcr
def test_card_transaction_retrieve_card():
    ct = CardTransaction.retrieve('CT00PARENT01')
    card = ct.card
    assert card
    assert card.user_id == ct.user_id
    assert len(card.number) == 16
