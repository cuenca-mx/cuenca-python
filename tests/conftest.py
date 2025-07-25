import datetime as dt
from io import BytesIO

import pytest
from cuenca_validations.types import Country, Gender, State
from cuenca_validations.types.enums import Profession

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
def curp_validation_request() -> dict:
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
def user_request() -> dict:
    user_dict = dict(
        curp='LOHJ660606HDFPRS02',
        phone_number='+525511223344',
        email_address='jose@test.com',
        profession=Profession.empleado,
        address=dict(
            street='calle 1',
            ext_number='2',
            int_number='3',
            postal_code_id='PC2ygq9j2bS9-9tsuVawzErA',
        ),
        phone_verification_id='VERdkuqOCjSA2PSS-VCj7HhQ',
        email_verification_id='VERppwdqsQSAQFFF-CDsWD8s',
    )
    return user_dict


@pytest.fixture
def user_lists_request() -> dict:
    user_dict = dict(
        curp='LOHJ660606HDFPRS02',
        names='Alejandro',
        first_surname='Martinez',
        second_surname='Viquez',
    )
    return user_dict


@pytest.fixture
def file() -> BytesIO:
    with open('tests/data/test_file.jpeg', 'rb') as image_file:
        return BytesIO(image_file.read())
