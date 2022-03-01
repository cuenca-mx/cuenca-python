import datetime as dt
from io import BytesIO
from typing import Dict

import pytest
from cuenca_validations.types import Country, Gender, State

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


@pytest.fixture
def curp_validation_request() -> Dict:
    curp_validation = dict(
        names='José',
        first_surname='López',
        second_surname='Hernández',
        date_of_birth=dt.date(1966, 6, 6),
        state_of_birth=State.DF,
        country_of_birth=Country.MX,
        gender=Gender.male,
    )
    return curp_validation


@pytest.fixture
def user_request() -> Dict:
    user_dict = dict(
        curp='LOHJ660606HDFPRS02',
        phone_number='+525511223344',
        email_address='jose@test.com',
        profession='employee',
        address=dict(
            street='calle 1',
            ext_number='2',
            int_number='3',
            postal_code='09900',
            state=State.DF.value,
            country=Country.MX,
        ),
    )
    return user_dict


@pytest.fixture
def file() -> BytesIO:
    with open('tests/data/test_file.jpeg', 'rb') as image_file:
        return BytesIO(image_file.read())
