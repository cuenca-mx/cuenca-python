import pytest

from cuenca import BalanceEntry
from cuenca.exc import CuencaResponseException


@pytest.mark.vcr
def test_balance_entry_retrieve():
    id_entry = 'TV01'
    balance_entry: BalanceEntry = BalanceEntry.retrieve(id_entry)
    assert balance_entry.id == id_entry
    txn = balance_entry.related_transaction
    assert (
        balance_entry.related_transaction_uri == f'/{txn._resource}/{txn.id}'
    )


@pytest.mark.vcr
def test_balance_entry_related_transaction_not_exist():
    id_entry = 'TV02'
    balance_entry: BalanceEntry = BalanceEntry.retrieve(id_entry)
    assert balance_entry.id == id_entry
    with pytest.raises(CuencaResponseException):
        balance_entry.related_transaction
