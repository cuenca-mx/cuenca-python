import datetime as dt

import pytest
from cuenca_validations.types import KYCFileType
from cuenca_validations.types.requests import UserRequest

from cuenca.resources.users import User


@pytest.mark.fixture
def user():
    user_dict = dict(
        nombres='Pedro',
        primer_apellido='Páramo',
        segundo_apellido='González',
        curp='APCURP123456HDHFHA',
        rfc='APCURP123456',
        gender='H',
        birth_date=dt.datetime(1917, 5, 16),
        birth_place='DF',
        birth_country='MX',
        terms_of_service=dict(
            version=1,
            ip='127.0.0.1',
            location='51.178829300000004,-1.8261830004623518',
            type='arteria',
        ),
        # para el user en sí
        phone_number='+525555555501',
        email_address='pedro_paramo@arteria.io',
        profession='student',
        platform_terms_of_service=dict(
            version=1,
            ip='127.0.0.1',
            location='51.178829300000004,-1.8261830004623518',
            type='cuenca',
        ),
        address=dict(
            calle='Reforma',
            numero_ext='265',
            numero_int='piso 5',
            codigo_postal='06500',
            estado='CDMX',
            ciudad='CDMX',
            colonia='Cuauhtemoc',
        ),
        govt_id=dict(
            type=KYCFileType.govt_id,
            feedme_uri_front='test.com',
            feedme_uri_back='test.com',
            is_mx=True,
        ),
        proof_of_address=dict(
            type=KYCFileType.proof_of_address,
            feedme_uri_front='test.com',
            feedme_uri_back='test.com',
            is_mx=True,
        ),
        proof_of_life=dict(
            type=KYCFileType.proof_of_life,
            feedme_uri_front='test.com',
            feedme_uri_back='test.com',
            is_mx=True,
        ),
    )
    req = UserRequest(**user_dict)
    user = User.create(req)

    yield user


# agregar test para update de los que se puedan
