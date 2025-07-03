import pytest

from cuenca.resources import PostalCodes


@pytest.mark.vcr
def test_postal_codes_retrieve_one_colony() -> None:
    postal_codes = list(PostalCodes.all(postal_code='40100'))
    assert len(postal_codes) == 1


@pytest.mark.vcr
def test_postal_codes_retrieve_multiple_colony() -> None:
    postal_codes = list(PostalCodes.all(postal_code='40106'))
    assert len(postal_codes) > 1


@pytest.mark.vcr
def test_postal_codes_retrieve_not_found() -> None:
    postal_codes = list(PostalCodes.all(postal_code='401000'))
    assert len(postal_codes) == 0
