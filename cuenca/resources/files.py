from io import BytesIO
from typing import ClassVar, cast

from cuenca_validations.types import (
    FileFormat,
    FileQuery,
    FileRequest,
    KYCFileType,
)
from pydantic import HttpUrl
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Downloadable, Queryable


@dataclass
class File(Creatable, Downloadable, Queryable):
    _resource: ClassVar = 'files'
    _query_params: ClassVar = FileQuery

    extension: str
    type: KYCFileType
    url: HttpUrl

    @classmethod
    def create(
        cls,
        file: BytesIO,
        *,
        session: Session = global_session,
    ) -> 'File':
        """
        Stores an encrypted version of the file,
        only users with permissions can access it.

        :param session:
        :return: New encrypted file object
        """
        req = FileRequest(file=file.read())
        response = session.post(
            endpoint=f'/{cls._resource}',
            data={},
            files=dict(file=req.file),
        )
        return cast('File', response)

    @property
    def file(self) -> bytes:
        """
        Bytes of the decrypted file.
        Format of the file is found on `file_type` property.
        """
        return self.download(self, file_format=FileFormat.any).read()

    @property
    def pdf(self) -> bytes:
        """
        Override property value for `Donwlodable`
        """
        return self.file

    @property
    def xml(self) -> bytes:
        """
        Override property value for `Donwlodable`
        """
        return self.file
