from datetime import datetime

import pytest
from cuenca_validations.types import DocumentType
from cuenca_validations.types.requests import DocumentRequest

from cuenca import ComercialDocument


@pytest.mark.vcr
def test_comercial_documents_create():
    document = ComercialDocument.create(
        DocumentRequest(
            client_name='Iron Man',
            clabe='32521352365236236',
            address='Address Foo',
            rfc='RFCXXXXXXXXX',
            date=datetime(2020, 11, 1),
            document_type=DocumentType.invoice,
        )
    )
    assert document.id is not None
    assert document.body is not None
