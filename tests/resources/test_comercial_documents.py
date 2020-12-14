import os
from datetime import date

import pytest
from cuenca_validations.types import DocumentType
from cuenca_validations.types.requests import DocumentRequest
from pydantic import ValidationError

from cuenca import ComercialDocument


@pytest.mark.vcr
def test_comercial_documents_create():
    document = ComercialDocument.create(
        DocumentRequest(
            client_name='Iron Man',
            clabe='002000000000000008',
            address='Address Foo',
            rfc='GODE561231GR8',
            date=(2020, 11),
            document_type=DocumentType.invoice,
        )
    )
    assert document.id is not None
    assert document.body is not None

    zip_name = 'CDceVNfKmzRH6PDgFnlHwgsg.zip'
    base_dir = os.path.abspath(os.getcwd())

    document.download(path=f'{base_dir}/tests/resources')

    assert os.path.exists(f'{base_dir}/tests/resources/{zip_name}')


def test_comercial_documents_create_errors():
    now = date.today()
    with pytest.raises(ValidationError) as exc_info:
        ComercialDocument.create(
            DocumentRequest(
                client_name='Iron Man',
                clabe='002000000000000008',
                address='Address Foo',
                rfc='fooo',
                date=(now.year, now.month),
                document_type=DocumentType.invoice,
            )
        )
    assert exc_info.value.errors()[0] == dict(
        loc=('rfc',),
        type='value_error',
        msg='Invalid rfc format',
    )
    assert exc_info.value.errors()[1] == dict(
        loc=('date',),
        type='value_error',
        msg='You cannot check the current month',
    )
