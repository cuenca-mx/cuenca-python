import pytest
from cuenca_validations.types import (
    CardFundingType,
    CardIssuer,
    CardStatus,
    CardType,
)

from cuenca.exc import CuencaResponseException, NoResultFound
from cuenca.resources import Card

user_id = 'US1237'
card_id = 'CAycvo_X9TQoKOKsaAvdqn3w'


@pytest.mark.vcr
def test_card_create():
    card = Card.create(CardIssuer.cuenca, CardFundingType.credit, user_id)
    assert card.id
    assert len(card.number) == 16
    assert card.type == CardType.virtual
    assert card.user_id == user_id


@pytest.mark.vcr
def test_can_not_assign_new_virtual_card():
    with pytest.raises(CuencaResponseException) as exc:
        Card.create(CardIssuer.cuenca, CardFundingType.credit, user_id)
    assert exc.value


@pytest.mark.vcr
def test_card_retrieve():
    card: Card = Card.retrieve(card_id)
    assert card.id == card_id
    assert len(card.number) == 16
    assert card.last_4_digits == '9849'
    assert card.bin == '544875'
    assert card.type == CardType.virtual
    assert not card.pin_attempts_exceeded


@pytest.mark.vcr
def test_card_not_found():
    with pytest.raises(CuencaResponseException) as exc:
        Card.retrieve('not-existing-id')
    assert exc.value.status_code == 404
    assert exc.value.json['Code'] == 'NotFoundError'


@pytest.mark.vcr
def test_card_one():
    card = Card.one(
        number='5448750078699849', exp_month=2, exp_year=2026, cvv2='353'
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
def test_card_update_pin():
    new_pin = '7AC814A636D901BE'
    card = Card.update(card_id, pin_block=new_pin)
    assert card


@pytest.mark.vcr
def test_deactivate_card():
    card = Card.deactivate(card_id)
    assert card.status == CardStatus.deactivated


@pytest.mark.vcr
def test_card_can_not_be_updated_if_it_is_deactivated():
    with pytest.raises(CuencaResponseException) as exc:
        Card.update(card_id, status=CardStatus.active)
    assert exc.value
