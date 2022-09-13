import pytest
from cuenca_validations.types import KYCFileType

from cuenca import File


@pytest.mark.vcr
def test_file_upload(file):
    uploaded_file: File = File.upload(
        file=file, file_type=KYCFileType.ine, extension='jpeg'
    )
    assert uploaded_file.id is not None
    assert uploaded_file.type == KYCFileType.ine
    assert uploaded_file.url is not None
    assert uploaded_file.user_id is not None


@pytest.mark.vcr
def test_file_download():
    file: File = File.first(type=KYCFileType.ine)
    assert isinstance(file.file, bytes)


@pytest.mark.vcr
def test_file_download_only_bytes():
    # Only download Bytes
    downloaded_file = File.download('EFXXX')
    assert isinstance(downloaded_file.read(), bytes)


@pytest.mark.vcr
def test_file_error_on_xml_pdf():
    file: File = File.first(type=KYCFileType.ine)
    with pytest.raises(NotImplementedError):
        file.xml

    with pytest.raises(NotImplementedError):
        file.pdf
