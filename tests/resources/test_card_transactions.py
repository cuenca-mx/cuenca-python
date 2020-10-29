import pytest

from cuenca import CardTransaction


@pytest.mark.vcr
def test_card_transaction_parent_retrieve():
    ct = CardTransaction.retrieve('CT001')
    related_cts = ct.related_card_transactions
    assert len(related_cts) == 3
    for card_transaction in related_cts:
        assert card_transaction.type != 'auth'


@pytest.mark.vcr
def test_card_transaction_child_retrieve():
    ct = CardTransaction.retrieve('CT002')
    related_cts = ct.related_card_transactions
    assert len(related_cts) == 1
    assert related_cts[0].type == 'auth'


@pytest.mark.vcr
def test_card_transaction_refund_without_parent_id_retrieve():
    ct = CardTransaction.retrieve('CT003')
    assert not ct.related_card_transactions


@pytest.mark.vcr
def test_card_transaction_expiration_retrieve():
    ct = CardTransaction.retrieve('CT004')
    assert ct.type == 'expiration'
