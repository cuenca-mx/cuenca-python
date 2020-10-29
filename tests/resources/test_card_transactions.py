import pytest

from cuenca import CardTransaction


@pytest.mark.vcr
def test_card_transaction_parent_retrieve():
    id_card_transaction = 'CT001'
    cardt: CardTransaction = CardTransaction.retrieve(id_card_transaction)
    assert cardt.id == id_card_transaction
    related_card_transactions = cardt.related_card_transactions
    assert len(related_card_transactions) == 2
    for card_transaction in related_card_transactions:
        assert card_transaction.type != 'auth'


@pytest.mark.vcr
def test_card_transaction_child_retrieve():
    id_card_transaction = 'CT002'
    cardt: CardTransaction = CardTransaction.retrieve(id_card_transaction)
    assert cardt.id == id_card_transaction
    related_card_transactions = cardt.related_card_transactions
    assert len(related_card_transactions) == 1
    assert related_card_transactions[0].type == 'auth'


@pytest.mark.vcr
def test_card_transaction_refund_without_parent_id_retrieve():
    id_card_transaction = 'CT003'
    cardt: CardTransaction = CardTransaction.retrieve(id_card_transaction)
    assert cardt.id == id_card_transaction
    assert not cardt.related_card_transactions


@pytest.mark.vcr
def test_card_transaction_expiration_retrieve():
    id_card_transaction = 'CT004'
    cardt: CardTransaction = CardTransaction.retrieve(id_card_transaction)
    assert cardt.id == id_card_transaction
    assert cardt.type == 'expiration'
