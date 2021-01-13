import pytest


@pytest.fixture
def cuenca_creds(monkeypatch) -> None:
    monkeypatch.setenv('CUENCA_API_KEY', 'api_key')
    monkeypatch.setenv('CUENCA_API_SECRET', 'secret')
