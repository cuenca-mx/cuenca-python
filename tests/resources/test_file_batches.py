import pytest
from cuenca_validations.types import KYCFileType

from cuenca import FileBatch


@pytest.mark.vcr
def test_file_batch_create():
    files = [
        dict(
            url='https://somefile.com/location=XXX1',
            type=KYCFileType.ine,
            is_back=True,
        ),
        dict(
            url='https://somefile.com/location=XXX2',
            type=KYCFileType.proof_of_liveness,
        ),
        dict(
            url='https://somefile.com/location=XXX3',
            type=KYCFileType.proof_of_address,
        ),
    ]
    user_id = 'US01'
    batch: FileBatch = FileBatch.create(files=files, user_id=user_id)
    assert batch.id is not None
    assert batch.received_files is not None
    assert batch.user_id == 'US01'
    assert len(batch.uploaded_files) == 3

    for file in batch.uploaded_files:
        assert file.id is not None
        assert file.url is not None
        if file.type == KYCFileType.ine:
            assert file.is_back
