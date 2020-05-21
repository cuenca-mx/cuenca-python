import datetime as dt

from cuenca.validators import QueryParams


def test_count():
    model = QueryParams(**dict(count=1))
    assert model.count
    model = QueryParams(**dict(count=True))
    assert model.count
    model = QueryParams(**dict(count=0))
    assert not model.count


def test_dict():
    date = dt.datetime.utcnow()
    model = QueryParams(**dict(count=1, created_before=date))
    assert model.dict() == dict(created_before=date)
