import pytest
from cuenca_validations.types import EventType

from cuenca import UserEvent


@pytest.mark.vcr
def test_user_event_retrieve():
    user_id = 'USCM-zlFcNQk6ue4gZ_mTGeQ'
    user_event = UserEvent.one(user_id=user_id, type=EventType.created)
    assert user_event.id is not None
