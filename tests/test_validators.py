import datetime as dt

import pytest

from cuenca.validators import QueryParams


@pytest.mark.parametrize(
    'count, truth',
    [
        (1, True),
        ('1', True),
        (True, True),
        (False, False),
        (0, False),
        ('0', False),
    ],
)
def test_count(count, truth):
    q = QueryParams(count=count)
    assert q.count is truth


def test_dict():
    now = dt.datetime.utcnow()
    model = QueryParams(count=1, created_before=now)
    assert model.dict() == dict(count=1, created_before=now.isoformat())
