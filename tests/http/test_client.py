import pytest
from requests import HTTPError

from cuenca.http import session


@pytest.mark.vcr
def test_invalid_auth():
    session.configure(sandbox=False)
    with pytest.raises(HTTPError):
        session.post('/api_keys', dict())
    session.configure(sandbox=True)
