import datetime as dt

from cuenca.types import SantizedDict, Status


def test_sanitized_dict():
    now = dt.datetime.now()
    assert SantizedDict(
        status=Status.succeeded, time=now, hello='there'
    ) == dict(status='succeeded', time=now.isoformat(), hello='there')
