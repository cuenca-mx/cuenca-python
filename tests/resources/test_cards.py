import datetime as dt

import pytest
from cuenca_validations.types import CardStatus, CardType
from pydantic import ValidationError

from cuenca.resources import Card


def test_update_card():
    card = Card(
        id='100',
        created_at=dt.datetime.now(),
        updated_at=dt.datetime.now(),
        user_id='US12344',
        ledger_account_id='LA123344',
        exp_month=3,
        exp_year=2021,
        card_number='4122000011112222',
        cvv2='123',
        type=CardType.virtual,
        status=CardStatus.created,
    )
    card.status = CardStatus.active
    updated_card = card.update()
    assert updated_card.status == CardStatus.active


def test_update_card_invalid_fields_should_fail():
    card = Card(
        id='100',
        created_at=dt.datetime.now(),
        updated_at=dt.datetime.now(),
        user_id='US12344',
        ledger_account_id='LA123344',
        exp_month=3,
        exp_year=2021,
        card_number='4122000011112222',
        cvv2='123',
        type=CardType.virtual,
        status=CardStatus.created,
    )
    card.card_number = '4122000011113333'
    with pytest.raises(ValidationError):
        card.update()
