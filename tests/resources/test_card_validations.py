import pytest

from cuenca.resources import CardValidation


@pytest.mark.vcr
def test_card_validations():
    card_data = dict(
        number='5448750129965637',
        cvv='685',
        cvv2='150',
        icvv='399',
        exp_month=2,
        exp_year=25,
        pin_block='3B241739AB05D290',
        pin_attempts_exceeded=True,
    )
    validation = CardValidation.create(**card_data)
    assert validation.is_active
    assert validation.card_uri is not None
    assert validation.is_valid_cvv
    assert validation.is_valid_cvv2
    assert validation.is_valid_icvv
    assert validation.is_valid_pin_block
    assert validation.is_valid_exp_date
    assert not validation.is_expired
    c = validation.card
    assert validation.card_id == c.id
    assert validation.is_active
    assert validation.is_pin_attempts_exceeded
