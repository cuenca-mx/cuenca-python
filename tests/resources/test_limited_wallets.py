import pytest

from cuenca import LimitedWallet


@pytest.mark.vcr
def test_limited_wallet_create():
    curp = 'TAXM840916HNEMXT02'
    rfc = 'TAXM840916123'
    wallet = LimitedWallet.create(allowed_curp=curp, allowed_rfc=rfc)
    assert wallet.id is not None
    assert wallet.balance == 0
    assert wallet.allowed_curp == curp
    assert wallet.allowed_rfc == rfc


@pytest.mark.vcr
def test_limited_wallet_retrieve():
    id = 'LA3vx08KlQCXsaP9qyWfb680'
    wallet = LimitedWallet.retrieve(id)
    assert wallet.id == id
