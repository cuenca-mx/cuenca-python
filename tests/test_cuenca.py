import requests_mock  # type: ignore

import cuenca


def test_get_balance():
    # It is the case when the user has transactions in the account
    response_json = {
        'items': [
            {
                'id': 'LE6xvD1ocHmSIu7MgzlC9woj',
                'created_at': '2021-08-17T21:45:23.061000',
                'user_id': 'US3zGWi1n852bTyqD1wCZ1ft',
                'name': 'RESTAURANT BRASIL MEXICO DF CMXMX',
                'amount': 1212,
                'descriptor': '',
                'rolling_balance': 7578889,
                'type': 'debit',
                'related_transaction_uri': '/card_transactions/CT3TA',
                'funding_instrument_uri': '/cards/CA243qFpGLDAaPamCMYHhS0p',
                'wallet_id': 'default',
            }
        ],
        'next_page_uri': None,
    }
    with requests_mock.mock() as m:
        m.get(
            'https://sandbox.cuenca.com/balance_entries?limit=1',
            status_code=200,
            json=response_json,
        )

        balance = cuenca.get_balance()
    assert balance == response_json['items'][0]['rolling_balance']


def test_get_balance_before_first_transaction():
    # When the user have no transactions at all
    # balance_entries endpoint returns `items` as empty list.
    # It means that its balance is Mx$0.00
    response_json = {'items': [], 'next_page_uri': None}

    with requests_mock.mock() as m:
        m.get(
            'https://sandbox.cuenca.com/balance_entries?limit=1',
            status_code=200,
            json=response_json,
        )

        balance = cuenca.get_balance()
    assert balance == 0
