import pytest

from cuenca import BalanceEntry
from cuenca.exc import CuencaResponseException


@pytest.mark.vcr
def test_balance_entry_retrieve():
    id_entry = 'TV01'
    balance_entry: BalanceEntry = BalanceEntry.retrieve(id_entry)
    assert balance_entry.id == id_entry
    # related_transaction
    txn = balance_entry.related_transaction
    assert (
        balance_entry.related_transaction_uri == f'/{txn._resource}/{txn.id}'
    )
    # funding_instrument
    bfi = balance_entry.funding_instrument
    assert balance_entry.funding_instrument_uri == f'/{bfi._resource}/{bfi.id}'
