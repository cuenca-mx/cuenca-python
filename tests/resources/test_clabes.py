import pytest

from cuenca import Clabe


@pytest.mark.vcr
def test_clabe_create():
    clabe = Clabe.create()
    assert clabe
    assert clabe.id
    assert clabe.clabe


@pytest.mark.vcr
def test_clabe_retrieve():
    clabe_id = 'CLD_zg463BQ6-yEjg8UE0jgQ'
    clabe = Clabe.retrieve(clabe_id)
    assert clabe
    assert clabe.id == clabe_id
    assert clabe.clabe


@pytest.mark.vcr
def test_clabe_all():
    clabes = list(Clabe.all())
    assert clabes
