import datetime as dt

import pytest
from cuenca_validations.types import SavingCategory

from cuenca import Saving


@pytest.mark.vcr
def test_saving_create():
    saving = Saving.create(
        name='my new car',
        category=SavingCategory.vehicle,
        goal_amount=100000,
        goal_date=(dt.datetime.utcnow() + dt.timedelta(days=365)),
    )
    assert saving.id is not None
    assert saving.is_active
    assert saving.balance == 0


@pytest.mark.vcr
def test_saving_retrieve():
    saving_id = 'lAob5rOC0jSj6UC5RAbwnSnA'
    saving = Saving.retrieve(saving_id)
    assert saving.id == saving_id


@pytest.mark.vcr
def test_saving_update():
    saving_id = 'lAob5rOC0jSj6UC5RAbwnSnA'
    changes = dict(
        name='my new home',
        goal_amount=200000,
        category=SavingCategory.home,
    )
    saving = Saving.update(saving_id, **changes)
    assert all(item in saving.to_dict().items() for item in changes.items())


@pytest.mark.vcr
def test_saving_deactivate():
    saving_id = 'lAob5rOC0jSj6UC5RAbwnSnA'
    saving = Saving.deactivate(saving_id)
    assert saving.deactivated_at is not None
