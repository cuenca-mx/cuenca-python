from typing import Generator

import pytest

from cuenca.http import session


@pytest.fixture(scope='module')
def vcr_config():
    config = dict()
    config['filter_headers'] = [('Authorization', 'DUMMY')]
    return config


@pytest.fixture
def test_client() -> Generator:
    session.configure(api_key='test', api_secret='test', sandbox=True)
    yield session
