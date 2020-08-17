import pytest


@pytest.fixture
def cuenca_creds(monkeypatch) -> None:
    monkeypatch.setenv('CUENCA_API_KEY', 'api_key')
    monkeypatch.setenv('CUENCA_API_SECRET', 'secret')


@pytest.fixture
def aws_creds(monkeypatch) -> None:
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'aws_key')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'aws_secret')
    monkeypatch.setenv('AWS_DEFAULT_REGION', 'us-east-1')
