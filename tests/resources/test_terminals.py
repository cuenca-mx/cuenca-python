import pytest
from pydantic import ValidationError

from cuenca import Terminal

# Creating terminals


@pytest.mark.vcr
def test_terminals_create_minimum():
    terminal = Terminal.create(brand_name='Tacos Pepe', slug='tacos-pepe',)
    assert terminal.id is not None
    assert terminal.created_at is not None
    assert terminal.updated_at is not None
    assert terminal.brand_name == 'Tacos Pepe'
    assert terminal.brand_image == ''
    assert terminal.slug == 'tacos-pepe'
    assert terminal.cash_active
    assert terminal.spei_active
    assert not terminal.card_active  # Card is inactive by default
    assert not terminal.stripe_ready  # Not ready by default


@pytest.mark.vcr
def test_terminals_create_full():
    terminal = Terminal.create(
        brand_name='Tacos Pepe',
        brand_image='https://s3.amazonaws.com/feedme.cuenca.io/abef8a6',
        slug='tacos-pepe',
        cash_active=False,
        spei_active=False,
    )
    assert terminal.id is not None
    assert terminal.created_at is not None
    assert terminal.updated_at is not None
    assert terminal.brand_name == 'Tacos Pepe'
    assert (
        terminal.brand_image
        == 'https://s3.amazonaws.com/feedme.cuenca.io/abef8a6'
    )
    assert terminal.slug == 'tacos-pepe'
    assert not terminal.cash_active
    assert not terminal.spei_active
    assert not terminal.card_active  # Card is inactive by default
    assert not terminal.stripe_ready  # Not ready by default


def test_terminals_cannot_create_with_invalid_attrs():

    # Invalid slug
    invalid_slugs = [
        'tacos@pepe',
        '1',
        'abc',
        '💳online',
        '494a-',
        'abcdefghijklmnopqrstuvwxyz',
    ]

    for _slug in invalid_slugs:
        with pytest.raises(ValidationError) as e:
            Terminal.create(
                brand_name='Tacos Pepe', slug=_slug,
            )
        assert 'string does not match regex' in str(e)


def test_terminals_cannot_create_without_required_attrs():

    valid_attrs = {
        'brand_name': 'Tacos Pepe',
        'slug': 'tacos-pepe',
    }

    # All attributes are required
    for attr in valid_attrs.keys():
        payload = valid_attrs.copy()
        del payload[attr]
        with pytest.raises(TypeError) as e:
            Terminal.create(**payload)
        assert f'missing 1 required positional argument: \'{attr}\'' in str(e)
