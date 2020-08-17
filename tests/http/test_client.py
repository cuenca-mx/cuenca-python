import pytest

from cuenca.exc import CuencaResponseException
from cuenca.http.client import Session


@pytest.mark.vcr
def test_invalid_auth():
    session = Session()
    session.configure(sandbox=False)
    with pytest.raises(CuencaResponseException) as e:
        session.post('/api_keys', dict())
    assert e.value.status_code == 401
    assert str(e.value)


@pytest.mark.usefixtures('cuenca_creds')
def test_basic_auth_configuration():
    session = Session()
    assert session.auth == session.basic_auth
    assert session.auth == ('api_key', 'secret')
    assert not session.iam_auth


@pytest.mark.usefixtures('cuenca_creds', 'aws_creds')
def test_gives_preference_to_basic_auth_configuration():
    session = Session()
    assert session.auth == session.basic_auth
    assert session.iam_auth


@pytest.mark.usefixtures('aws_creds')
def test_aws_iam_auth_configuration():
    session = Session()
    assert session.auth == session.iam_auth


def test_configures_new_aws_creds():
    session = Session()
    session.configure(
        aws_access_key='new_aws_key', aws_secret_access_key='new_aws_secret'
    )
    assert session.auth.aws_secret_access_key == 'new_aws_secret'
    assert session.auth.aws_access_key == 'new_aws_key'
    assert session.auth.aws_region == 'us-east-1'


@pytest.mark.usefixtures('aws_creds')
def test_overrides_aws_creds():
    session = Session()
    session.configure(
        aws_access_key='new_aws_key',
        aws_secret_access_key='new_aws_secret',
        aws_region='us-east-2',
    )
    assert session.auth.aws_secret_access_key == 'new_aws_secret'
    assert session.auth.aws_access_key == 'new_aws_key'
    assert session.auth.aws_region == 'us-east-2'
