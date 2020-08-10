import pytest
from cuenca_validations.types import CardStatus, CardType

from cuenca.exc import CuencaResponseException, NoResultFound
from cuenca.resources import Card

user_id = 'US1237'
ledger_account_id = 'LA1237'
card_id = 'CA5x_xAHmYSE2DXhia0G0DTA'


@pytest.mark.vcr
def test_card_create() -> None:
    card = Card.create(ledger_account_id, user_id)
    assert card.id
    assert len(card.number) == 16
    assert card.type == CardType.virtual
    assert card.user_id == user_id
    assert card.ledger_account_id == ledger_account_id


@pytest.mark.vcr
def test_can_not_assign_new_virtual_card() -> None:
    with pytest.raises(CuencaResponseException) as exc:
        Card.create(ledger_account_id, user_id)
    assert exc.value


@pytest.mark.vcr
def test_card_retrieve() -> None:
    card: Card = Card.retrieve(card_id)
    assert card.id == card_id
    assert len(card.number) == 16
    assert card.type == CardType.virtual


@pytest.mark.vcr
def test_card_not_found() -> None:
    with pytest.raises(CuencaResponseException) as exc:
        Card.retrieve('not-existing-id')
    assert exc.value.status_code == 404
    assert exc.value.json['Code'] == 'NotFoundError'


@pytest.mark.vcr
def test_card_one() -> None:
    card = Card.one(
        number='4231450155147929', exp_month=8, exp_year=2026, cvv2='144'
    )
    assert card.id


@pytest.mark.vcr
def test_card_one_errors() -> None:
    with pytest.raises(NoResultFound):
        Card.one(user_id='fake id')


@pytest.mark.vcr
def test_card_all() -> None:
    cards = Card.all(user_id=user_id)
    assert len([cards]) == 1


@pytest.mark.vcr
def test_card_update() -> None:
    card = Card.update(card_id, status=CardStatus.blocked)
    assert card.status == CardStatus.blocked
    card = Card.update(card_id, status=CardStatus.active)
    assert card.status == CardStatus.active
