import pytest

from cuenca.resources import CardValidation


@pytest.mark.skip(reason="Not ready")
def test_card_validations():
    card_data = dict(
        number='5448750129965637',
        cvv='685',
        cvv2='150',
        icvv='399',
        exp_month=2,
        exp_year=25,
        pin_block='B57D25D49FD1F88A',
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
