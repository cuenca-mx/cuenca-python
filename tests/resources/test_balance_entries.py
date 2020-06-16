import pytest

from cuenca import BalanceEntry


@pytest.mark.vcr
def test_balance_entry_retrieve():
    id_entry = 'TV01'
    balance_entry: BalanceEntry = BalanceEntry.retrieve(id_entry)
    assert balance_entry.id == id_entry

    transaction = balance_entry.transaction
    assert transaction.id in balance_entry.transaction_uri

    # Second call don't produce a new request
    transaction = balance_entry.transaction
