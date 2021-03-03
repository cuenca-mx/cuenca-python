import pytest

from cuenca import UserCredential
from cuenca.http import Session


def test_update_password():
    UserCredential.create(password='222222')
    UserCredential.update(password=None)
    UserCredential.update(password='111111')


@pytest.mark.vcr
def test_block_user():
    session = Session()
    session.configure(
        'AKQErTmwedQqCLpCjeZG8sJQ',
        'KvL_oJXX071bduBaYdMOnWLZEnE-pE7UmBiqpQ'
        'F5QhrNlwQ6RVAP_RP1DWnNK5Jrf0uUuScmflCTBcJ4QxTRTw',
        sandbox=True,
        use_jwt=True,
    )
    UserCredential.update(
        'US46cuHpEJ5xFTOceMKVqSzF', is_active=False, session=session
    )
    UserCredential.update(
        'US46cuHpEJ5xFTOceMKVqSzF', is_active=True, session=session
    )
