import pytest

from cuenca import Endpoint
from cuenca.http.client import Session


@pytest.mark.vcr
def test_endpoint_retrieve():
    id_endpoint = 'EN01'
    endpoint: Endpoint = Endpoint.retrieve(id_endpoint)
    assert endpoint.id == id_endpoint
    assert endpoint.url
    assert endpoint.events
    assert not endpoint.deactivated_at


@pytest.mark.vcr
def test_endpoint_create():
    endpoint: Endpoint = Endpoint.create(url='https://url.com')
    assert endpoint.id
    assert endpoint.events
    assert endpoint.is_active
    assert endpoint.url
    assert not endpoint.deactivated_at


@pytest.mark.vcr
def test_endpoint_update():
    id_endpoint = 'EN02'
    endpoint: Endpoint = Endpoint.update(
        endpoint_id=id_endpoint,
        url='https://url.io',
        is_active=False
    )
    assert endpoint.id == id_endpoint
    assert endpoint.events
    assert endpoint.url == 'https://url.io'
    assert not endpoint.is_active
    assert not endpoint.deactivated_at


@pytest.mark.vcr
def test_endpoint_deactivate():
    id_endpoint = 'EN02'
    endpoint: Endpoint = Endpoint.deactivate(
        endpoint_id=id_endpoint
    )
    assert endpoint.id == id_endpoint
    assert endpoint.deactivated_at
