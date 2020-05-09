import pytest

from typing import Generator
from cuenca.http import session


@pytest.fixture
def test_client() -> Generator:
    session.configure(api_key='test', api_secret='test', sandbox=True)
    yield session

