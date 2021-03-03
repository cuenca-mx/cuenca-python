import pytest

from cuenca import BalanceEntry


@pytest.mark.vcr
def test_balance_entry_retrieve():
    id_entry = 'TV01'
    balance_entry: BalanceEntry = BalanceEntry.retrieve(id_entry)
    assert balance_entry.id == id_entry
    assert balance_entry.related_transaction
    assert balance_entry.funding_instrument
