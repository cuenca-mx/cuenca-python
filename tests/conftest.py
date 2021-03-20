import pytest

import cuenca

cuenca.configure(sandbox=True)


@pytest.fixture(scope='module')
def vcr_config():
    config = dict()
    config['filter_headers'] = [
        ('Authorization', 'DUMMY'),
        ('X-Cuenca-Token', 'DUMMY'),
    ]
    return config


@pytest.fixture
def transfer():
    yield cuenca.Transfer.create(
        account_number='646180157034181180',
        amount=10000,
        descriptor='first transfer',
        recipient_name='Frida Kahlo',
    )
