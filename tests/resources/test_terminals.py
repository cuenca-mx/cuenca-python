from typing import Dict, List

import pytest
from pydantic import ValidationError

from cuenca import Terminal
from cuenca.exc import NoResultFound

sample_image = (
    "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAACXBIWXMAA"
    "AsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAvSURBVHgB7c"
    "0xAQAgCAAwtJcBDER+iMDJsxXYeT8rFtxYIhaLxWKxWCwWi8XiWQO6BwI2GFK7OAAA"
    "AABJRU5ErkJggg=="
)

# Querying terminals


@pytest.mark.vcr
def test_terminals_query_slug():
    slug: str = 'tacos-pepe'
    terminal: Terminal = Terminal.one(slug=slug)
    assert terminal.slug == slug


@pytest.mark.vcr
def test_terminals_query_user_id():
    terminal: Terminal = Terminal.one(user_id='US303951')
    assert terminal.id is not None


@pytest.mark.vcr
def test_terminals_errors():
    with pytest.raises(NoResultFound):
        Terminal.one(slug='invalid')


@pytest.mark.vcr
def test_terminals_first():
    terminal: Terminal = Terminal.first(slug='tacos-pepe')
    assert terminal is not None
    assert terminal.slug == 'tacos-pepe'
    terminal = Terminal.first(user_id='invalid')
    assert terminal is None


@pytest.mark.vcr
def test_terminals_count():
    # Count with filter
    count: int = Terminal.count(slug='tacos-pepe')
    assert count == 1

    # Count all items is not allowed for this resource
    with pytest.raises(TypeError) as e:
        Terminal.count()
    assert 'you must pass a query parameter for this resource.' in str(e)


@pytest.mark.vcr
def test_terminals_all_method_not_allowed():
    with pytest.raises(NotImplementedError) as e:
        Terminal.all()
    assert 'not supported for this resource.' in str(e)


# Retrieving terminals


@pytest.mark.vcr
def test_terminals_retrieve():
    terminal_id: str = 'TRykH9-lXrS6iJocclOl4ATQ=='
    terminal: Terminal = Terminal.retrieve(terminal_id)
    assert terminal.id == terminal_id


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
        brand_image=open('tests/resources/test-image.png', 'rb').read(),
        slug='tacos-pepe',
        cash_active=False,
        spei_active=False,
    )
    assert terminal.id is not None
    assert terminal.created_at is not None
    assert terminal.updated_at is not None
    assert terminal.brand_name == 'Tacos Pepe'
    assert terminal.brand_image == sample_image
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
        terminal_id,
        slug='tacos-y-jugos-pepe',
        brand_name='Tacos y Jugos Pepe',
        brand_image=open('tests/resources/test-image.png', 'rb').read(),
        cash_active=True,
        spei_active=True,
        card_active=True,
    )
    assert terminal.id == terminal_id
    assert terminal.created_at is not None
    assert terminal.updated_at is not None
    assert terminal.brand_name == 'Tacos y Jugos Pepe'
    assert terminal.brand_image == sample_image
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
