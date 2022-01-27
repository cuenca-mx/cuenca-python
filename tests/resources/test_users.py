import pytest
from cuenca_validations.types import UserRequest, State

from cuenca.resources.users import User


@pytest.mark.fixture
def user_req():
    user_dict = dict(
        curp='LOPJ920604HDFPRS06',
        phone_number='+525559610838',
        email_address='email@email.com',
        profession='employee',
        address=dict(
            street='calle 1',
            ext_number='2',
            int_number='3',
            postal_code='09900',
            state=State.DF.value,
            country='Obrera',
        ),
    )
    req = UserRequest(**user_dict)
    yield req


def test_update_values(user_req):
    user = User.create(user_req)
