from io import BytesIO
from typing import ClassVar, Optional, cast

from cuenca_validations.types import (
    FileExtension,
    FileQuery,
    FileUploadRequest,
    KYCFileType,
)
from pydantic import HttpUrl

from ..http import Session, session as global_session
from .base import Downloadable, Queryable, Uploadable


class File(Downloadable, Queryable, Uploadable):
    _resource: ClassVar = 'files'
    _query_params: ClassVar = FileQuery

    extension: str
    type: KYCFileType
    url: HttpUrl
    user_id: str

    @classmethod
    def upload(
        cls,
        file: BytesIO,
        file_type: KYCFileType,
        extension: Optional[str],
        is_back: bool = False,
        user_id: str = 'me',
        *,
        session: Session = global_session,
    ) -> 'File':
        """
        Stores an encrypted version of the file,
        only users with permissions can access it.

        :param file:
        :param user_id:
        :param session:
        :return: New encrypted file object
        """
        req = FileUploadRequest(
            file=file.read(),
            type=file_type,
            extension=cast(FileExtension, extension),
            is_back=is_back,
            user_id=user_id,
        )
        return cast(
            'File',
            cls._upload(
                session=session,
                **req.model_dump(),
            ),
        )

    @property
    def file(self) -> bytes:
        """
        Bytes of the decrypted file.
        Format of the file is found on `file_type` property.
        """
        return self.download(self.id).read()

    @property
    def pdf(self) -> bytes:
        """
        Override from `Downloadable`, this property does not apply.
        """
        raise NotImplementedError

    @property
    def xml(self) -> bytes:
        """
        Override from `Downloadable`, this property does not apply.
        """
        raise NotImplementedError
