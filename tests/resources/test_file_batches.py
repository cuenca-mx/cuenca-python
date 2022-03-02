import pytest
from cuenca_validations.types import KYCFileType

from cuenca import FileBatch


@pytest.mark.vcr
def test_file_batch_create():
    files = [
        dict(
            url='https://media.getmati.com/file?location=XX1',
            type=KYCFileType.ine,
        ),
        dict(
            url='https://media.getmati.com/file?location=XX2',
            type=KYCFileType.proof_of_liveness,
        ),
        dict(
            url='https://media.getmati.com/file?location=XX3',
            type=KYCFileType.proof_of_address,
        ),
    ]
    user_id = 'US01'
    batch: FileBatch = FileBatch.create(files=files, user_id=user_id)
    assert batch.id is not None
    assert batch.received_files is not None
    assert KYCFileType.ine in batch.uploaded_files
    assert KYCFileType.proof_of_liveness in batch.uploaded_files
    assert KYCFileType.proof_of_address in batch.uploaded_files
    assert batch.user_id == 'US01'
