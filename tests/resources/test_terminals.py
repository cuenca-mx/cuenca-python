from typing import Dict, List

import pytest
from pydantic import ValidationError

from cuenca import Terminal

# Creating terminals


@pytest.mark.vcr
def test_terminals_create_minimum():
    terminal: Terminal = Terminal.create(
        brand_name='Tacos Pepe', slug='tacos-pepe',
    )
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
    terminal: Terminal = Terminal.create(
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
    invalid_slugs: List = [
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

    valid_attrs: Dict = {
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


# Updating terminals


@pytest.mark.vcr
def test_terminals_update_full():
    terminal_id = 'TR000396'
    terminal: Terminal = Terminal.update(
        terminal_id, slug='tacos-y-jugos-pepe', brand_name='Tacos y Jugos Pepe', brand_image='https://s3.amazonaws.com/feedme.cuenca.io/abc123', cash_active=True, spei_active=True, card_active=True,
    )
    assert terminal.id == terminal_id
    assert terminal.created_at is not None
    assert terminal.updated_at is not None
    assert terminal.brand_name == 'Tacos y Jugos Pepe'
    assert terminal.brand_image == 'https://s3.amazonaws.com/feedme.cuenca.io/abc123'
    assert terminal.slug == 'tacos-y-jugos-pepe'
    assert terminal.cash_active
    assert terminal.spei_active
    assert terminal.card_active
    assert terminal.stripe_ready


@pytest.mark.vcr
def test_terminals_update_partial():
    terminal_id = 'TR000391'
    terminal: Terminal = Terminal.update(
        terminal_id, slug='tacos-y-jugos-pepe'
    )
    assert terminal.id == terminal_id
    assert terminal.created_at is not None
    assert terminal.updated_at is not None
    assert terminal.brand_name == 'Tacos Pepe'
    assert terminal.slug == 'tacos-y-jugos-pepe'


def test_terminals_cannot_update_with_invalid_attrs():

    # Invalid slug
    invalid_slugs: List = [
        'tacos@pepe',
        '1',
        'abc',
        '💳online',
        '494a-',
        'abcdefghijklmnopqrstuvwxyz',
    ]

    for _slug in invalid_slugs:
        with pytest.raises(ValidationError) as e:
            Terminal.update(
                id="TR123", slug=_slug,
            )
        assert 'string does not match regex' in str(e)

    # Read-only attrs
    with pytest.raises(TypeError) as e:
        Terminal.update(
            id="TR123", updated_at="today",
        )
    assert ' got an unexpected keyword argument' in str(e)
