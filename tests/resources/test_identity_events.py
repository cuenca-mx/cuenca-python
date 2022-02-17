import pytest
from cuenca_validations.types import EventType

from cuenca import IdentityEvent


@pytest.mark.vcr
def test_identity_event_retrieve():
    identity_id = 'IDKWLi_wUoTty6WXXg9xfKFQ'
    identity_event = IdentityEvent.one(
        identity_id=identity_id, type=EventType.created.value
    )
    assert identity_event.id is not None
