import pytest

import cuenca
from cuenca import Clabe

LEGAL_PERSON_ID = 'USmI9NnHJXTKi9ILP1aaWjlQ'
ALLOWED_CURP_RFC = 'LOPJ900101XXX'


@pytest.mark.vcr
def test_clabe_create():
    clabe = Clabe.create(LEGAL_PERSON_ID, ALLOWED_CURP_RFC)
    assert clabe.id
    assert clabe.clabe
    assert clabe.user_id == LEGAL_PERSON_ID
    assert clabe.allowed_curp_rfc == ALLOWED_CURP_RFC
    assert clabe.is_default is False


@pytest.mark.vcr
def test_clabe_all():
    clabes = list(Clabe.all(allowed_curp_rfc=ALLOWED_CURP_RFC))
    assert clabes
    assert clabes[0].allowed_curp_rfc == ALLOWED_CURP_RFC
    assert clabes[0].is_default is False
