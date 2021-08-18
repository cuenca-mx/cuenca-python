import pytest

import cuenca


@pytest.mark.vcr
def test_get_balance():
    balance = cuenca.get_balance()
    assert balance > 0


@pytest.mark.vcr
def test_get_balance_before_first_transaction():
    balance = cuenca.get_balance()
    assert balance == 0
