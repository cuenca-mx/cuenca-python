import datetime as dt
import json
from typing import ClassVar, cast

from clabe import Clabe
from cuenca_validations.types import DocumentType
from cuenca_validations.types.requests import DocumentRequest
from pydantic.dataclasses import dataclass

from .base import Creatable


@dataclass
class ComercialDocument(Creatable):
    _resource: ClassVar = 'documents'

    body: str

    @classmethod
    def create(
        cls,
        client_name: str,
        clabe: Clabe,
        address: str,
        rfc: str,
        date: dt.datetime,
        document_type: DocumentType,
    ) -> 'ComercialDocument':
        req = DocumentRequest(
            client_name=client_name,
            clabe=clabe,
            address=address,
            rfc=rfc,
            date=date,
            document_type=document_type,
        )
        return cast('ComercialDocument', cls._create(**json.loads(req.json())))
