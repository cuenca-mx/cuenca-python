import pytest

from cuenca.resources import ARPC


@pytest.mark.skip(reason="Not ready")
def test_arpc():
    arpc_req = dict(
        number='1234567890123403',
        arqc='test_arqc',
        key_derivation_method='3',
        arpc_method='1',
        txn_data='justsomerandomdata',
        arc='arc',
        pan_sequence='00',
        unique_number='number',
        atc='atc',
    )
    arpc = ARPC.create(**arpc_req)
    assert arpc.is_valid_arqc
