import pytest
from pydantic import ValidationError

from cuenca import Terminal

# Creating terminals


@pytest.mark.vcr
def test_terminals_create():
    terminal = Terminal.create(brand_name="Tacos Pepe", slug="tacos-pepe",)
    assert terminal.id is not None


def test_terminals_cannot_create_with_invalid_attributes():

    with pytest.raises(ValidationError) as e:
        Terminal.create(
            brand_name="Tacos Pepe", slug="tacos@pepe",
        )
    assert "string does not match regex" in str(e)
