import pytest

from cuenca.resources import Arpc


@pytest.mark.vcr
def test_arpc():
    arpc_req = dict(
        number='1234567890123403',
        arqc='DB3C77D5469C53C6',
        arpc_method='1',
        transaction_data='somerandomtransactiondata',
        response_code='0010',
        pan_sequence='01',
        unique_number='42D6A016',
        transaction_counter='001D',
        track_data_method='terminal',
    )
    arpc = Arpc.create(**arpc_req)
    assert arpc.is_valid_arqc
