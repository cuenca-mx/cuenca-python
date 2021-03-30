import pytest
from cuenca_validations.errors import TooManyAttemptsError
from cuenca_validations.types import CardStatus

from cuenca.resources import CardActivation


@pytest.mark.vcr
def test_card_activation():
    values = dict(
        number='4122943400023502',
        exp_month=11,
        exp_year=24,
        cvv2='123',
    )
    card_activation = CardActivation.create(**values)
    assert card_activation.success
    assert card_activation.user_id == 'US1237'
    card = card_activation.card
    assert all(getattr(card, key) == value for key, value in values.items())
    assert card.user_id == 'US1237'
    assert card.status is CardStatus.active


@pytest.mark.vcr
def test_blocked_attemps():
    values = dict(
        number='4122943499999999',
        exp_month=11,
        exp_year=24,
        cvv2='123',
    )
    for _ in range(6):
        activation = CardActivation.create(**values)
        assert activation.success is False
    with pytest.raises(TooManyAttemptsError):
        CardActivation.create(**values)
