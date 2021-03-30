import cuenca
from cuenca import session
from cuenca.resources import ARPC


def test_arpc():
    session.host = 'stage.cuenca.com'
    api_key = 'AK36EAQXIlurg53pRjcvtx30'
    api_secret = 'Ea-6JmpnRX3ZKi4oGHpsmroGEEPU1vgu2Eq362B27KiJG2aLGkuGh3pYfG725yDSNxQn0L92zCoFvEdnrr1Ybw'
    cuenca.configure(api_key=api_key, api_secret=api_secret)
    arpc_req = dict(
        arqc='test_arqc',
        key_derivation_method='3',
        arpc_method='1',
        txn_data='justsomerandomdata',
        card_id='CA1234',
        arc='arc',
        pan_sequence='00',
        unique_number='number',
        atc='atc',
    )
    arpc = ARPC.create(**arpc_req)
    assert arpc.is_valid_arqc
