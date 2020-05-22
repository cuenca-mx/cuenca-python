import pytest
from requests import HTTPError

from cuenca.http.client import Session


@pytest.mark.vcr
def test_invalid_auth():
    session = Session()
    session.configure(sandbox=False)
    with pytest.raises(HTTPError) as e:
        session.post('/api_keys', dict())
    assert '401 Client Error: Unauthorized' in str(e)
