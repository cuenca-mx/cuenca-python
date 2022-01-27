import pytest
from cuenca_validations.types.requests import UserRequest

from cuenca.resources.users import User


@pytest.mark.fixture
def user_req():
    user_dict = dict(
        curp='APCURP123456HDHFHA',
        # para el user en sí
        phone_number='+525555555501',
        email_address='pedro_paramo@arteria.io',
        profession='student',
        address=dict(
            calle='Reforma',
            numero_ext='265',
            numero_int='piso 5',
            codigo_postal='06500',
            estado='CDMX',
            ciudad='CDMX',
            colonia='Cuauhtemoc',
        ),
    )
    req = UserRequest(**user_dict)
    yield req


def test_update_values(user_req):
    user = User.create(user_req)
