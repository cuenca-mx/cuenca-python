import pytest
import requests_mock  # type: ignore

import cuenca


@pytest.mark.vcr
def test_get_balance():
    # It is the case when the user has transactions in the account
    balance = cuenca.get_balance()
    assert balance == 7578889


def test_get_balance_before_first_transaction():
    # When the user have no transactions at all
    # api.cuenca.com returns `items` as empty list.
    # It means that its balance is Mx$0.00

    with requests_mock.mock() as m:
        response_json = {'items': [], 'next_page_uri': None}
        m.get(
            'https://sandbox.cuenca.com/balance_entries?limit=1',
            status_code=200,
            json=response_json,
        )

        balance = cuenca.get_balance()
    assert balance == 0
