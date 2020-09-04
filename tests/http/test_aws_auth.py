import pytest
from requests.models import Request

from cuenca.http.aws_auth import get_canonical_path


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            Request(url='https://stage.cuenca.com/transfers'),
            '/oaxaca/transfers',
        ),
        (
            Request(url='https://stage.cuenca.com/transfers/TESTING'),
            '/oaxaca/transfers/TESTING',
        ),
        (Request(url='https://stage.cuenca.com/cards'), '/knox/cards'),
        (
            Request(url='https://stage.cuenca.com/cards/TESTING'),
            '/knox/cards/TESTING',
        ),
        (Request(url='https://stage.cuenca.com'), '/'),
    ],
)
def test_aws_auth(test_input, expected):
    assert get_canonical_path(test_input) == expected
