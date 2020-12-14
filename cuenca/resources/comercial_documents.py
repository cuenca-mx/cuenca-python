import base64
import json
import os
from typing import ClassVar, cast

from cuenca_validations.types.requests import DocumentRequest
from pydantic.dataclasses import dataclass

from .base import Creatable


@dataclass
class ComercialDocument(Creatable):
    _resource: ClassVar = 'comercial_documents'

    body: str

    @classmethod
    def create(cls, request: DocumentRequest) -> 'ComercialDocument':
        return cast(
            'ComercialDocument', cls._create(**json.loads(request.json()))
        )

    def download(cls, path: str = os.path.abspath(os.getcwd())):
        zip_file = open(f'{path}/{cls.id}.zip', "wb")
        zip_file.write(base64.b64decode(cls.body.encode("utf-8")))
        zip_file.close()
