import pytest
from cuenca_validations.types import CardStatus, CardType

from cuenca.exc import CuencaResponseException, NoResultFound
from cuenca.resources import Card

user_id = 'US1237'
ledger_account_id = 'LA1237'
card_id = 'CA5x_xAHmYSE2DXhia0G0DTA'


@pytest.mark.vcr
def test_card_create():
    card = Card.create(ledger_account_id, user_id)
    assert card.id
    assert len(card.number) == 16
    assert card.type == CardType.virtual
    assert card.user_id == user_id
    assert card.ledger_account_id == ledger_account_id


@pytest.mark.vcr
def test_can_not_assign_new_virtual_card():
    with pytest.raises(CuencaResponseException) as exc:
        Card.create(ledger_account_id, user_id)
    assert exc.value


@pytest.mark.vcr
def test_card_retrieve():
    card: Card = Card.retrieve(card_id)
    assert card.id == card_id
    assert len(card.number) == 16
    assert card.type == CardType.virtual


@pytest.mark.vcr
def test_card_not_found():
    with pytest.raises(CuencaResponseException) as exc:
        Card.retrieve('not-existing-id')
    assert exc.value.status_code == 404
    assert exc.value.json['Code'] == 'NotFoundError'


@pytest.mark.vcr
def test_card_one():
    card = Card.one(
        number='4231450155147929', exp_month=8, exp_year=2026, cvv2='144'
    )
    assert card.id


@pytest.mark.vcr
def test_card_one_errors():
    with pytest.raises(NoResultFound):
        Card.one(user_id='fake id')


@pytest.mark.vcr
def test_card_all():
    cards = Card.all(user_id=user_id)
    assert len(list(cards)) == 1


@pytest.mark.vcr
def test_card_update():
    card = Card.update(card_id, status=CardStatus.blocked)
    assert card.status == CardStatus.blocked
    card = Card.update(card_id, status=CardStatus.active)
    assert card.status == CardStatus.active


@pytest.mark.vcr
def test_deactivate_card():
    card = Card.deactivate(card_id)
    assert card.status == CardStatus.deactivated


@pytest.mark.vcr
def test_card_can_not_be_updated_if_it_is_deactivated():
    with pytest.raises(CuencaResponseException) as exc:
        Card.update(card_id, status=CardStatus.active)
    assert exc.value
