import hashlib
from unittest.mock import Mock, patch

import pytest
import requests
from freezegun import freeze_time  # type: ignore
from requests.models import Request, Response

from cuenca.http.aws_auth import CuencaAWSRequestAuth

ROUTES_CONFIG = dict(default_route='/oaxaca', routes=dict(cards='/knox'))


@pytest.fixture
def mock_configuration():
    with patch.object(Response, 'json', return_value=ROUTES_CONFIG):
        with patch.object(requests, 'get', return_value=Response()):
            yield


@pytest.fixture
def auth():
    return CuencaAWSRequestAuth(
        aws_access_key='testing_key',
        aws_secret_access_key='testing_secret',
        aws_region='us-east-1',
        aws_service='execute-api',
        aws_host='stage.cuenca.com',
    )


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
def test_aws_auth(test_input, expected, mock_configuration, auth):
    assert auth.get_canonical_path(test_input) == expected


@freeze_time("2020-11-25 03:00:00")
def test_auth(auth):
    url = (
        'https://stage.cuenca.com/transfers?idempotency_key=key_1&'
        'user_id=123&created_after'
    )
    mock_request = Mock()
    mock_request.url = url
    mock_request.method = "GET"
    mock_request.body = None
    mock_request.headers = {}

    auth(mock_request)
    assert {
        'Authorization': 'AWS4-HMAC-SHA256 Credential=testing_key/20201125/'
        'us-east-1/execute-api/aws4_request, SignedHeaders'
        '=host;x-amz-date, Signature=61bbed824d3bb736d4622'
        '47601f2d9f15ebe36994f1782172be23044250322bd',
        'x-amz-date': '20201125T030000Z',
        'x-amz-content-sha256': hashlib.sha256(b'').hexdigest(),
    } == mock_request.headers
