import pytest

from cuenca.resources.resources import retrieve_uri


def test_retrieve_wrong_uri():
    with pytest.raises(ValueError):
        retrieve_uri('wrong_uri')
