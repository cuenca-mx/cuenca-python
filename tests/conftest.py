import datetime as dt

import pytest
from cuenca_validations.types import (
    CurpValidationRequest,
    Gender,
    State,
    UserRequest,
)

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
def curp_validation_request() -> CurpValidationRequest:
    curp_validation = dict(
        names='Manuel',
        first_surname='Avalos',
        second_surname='Tovar',
        date_of_birth=dt.date(1997, 3, 29).isoformat(),
        state_of_birth=State.DF.value,
        country_of_birth='MX',
        gender=Gender.male,
    )
    return CurpValidationRequest(**curp_validation)


@pytest.fixture
def user_request() -> UserRequest:
    user_dict = dict(
        curp='AATM970329HDFVVN05',
        phone_number='+525559610838',
        email_address='manuel@cuenca.com',
        profession='employee',
        address=dict(
            street='calle 1',
            ext_number='2',
            int_number='3',
            postal_code='09900',
            state=State.DF.value,
            country='MEX',
        ),
    )
    return UserRequest(**user_dict)
