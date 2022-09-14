import pytest

from cuenca import Endpoint
from cuenca.exc import CuencaResponseException


@pytest.mark.vcr
def test_endpoint_retrieve():
    id_endpoint = 'EN01'
    endpoint: Endpoint = Endpoint.retrieve(id_endpoint)
    assert endpoint.id == id_endpoint
    assert endpoint.url
    assert endpoint.events
    assert endpoint.is_active


@pytest.mark.vcr
def test_endpoint_create():
    endpoint: Endpoint = Endpoint.create(url='https://url.com')
    assert endpoint.id
    assert endpoint.events
    assert endpoint.is_enable
    assert endpoint.url
    assert endpoint.is_active


@pytest.mark.vcr
def test_endpoint_create_another():
    with pytest.raises(CuencaResponseException) as exc:
        Endpoint.create(url='https://url.xyz')
        assert exc.value
        assert exc.json['error'] == 'Usuario ya tiene webhook asociado'


@pytest.mark.vcr
def test_endpoint_update():
    id_endpoint = 'EN02'
    endpoint: Endpoint = Endpoint.update(
        endpoint_id=id_endpoint,
        url='https://url.io',
        is_enable=False,
        events=['user.create', 'cash_deposit.create'],
    )
    assert endpoint.id == id_endpoint
    assert len(endpoint.events) == 2
    assert endpoint.url == 'https://url.io'
    assert not endpoint.is_enable
    assert endpoint.is_active


@pytest.mark.vcr
def test_endpoint_deactivate():
    id_endpoint = 'EN02'
    endpoint: Endpoint = Endpoint.deactivate(id_endpoint)
    assert endpoint.id == id_endpoint
    assert not endpoint.is_active
