import pytest

from cuenca.resources import PostalCodes


@pytest.mark.vcr
@pytest.mark.parametrize(
    "postal_code,expected_count",
    [
        ("40100", 1),
        ("40106", 2),
        ("00000", 0),
    ],
)
def test_postal_codes_retrieve(postal_code: str, expected_count: int) -> None:
    postal_codes = list(PostalCodes.all(postal_code=postal_code))
    assert len(postal_codes) == expected_count
