from typing import ClassVar

from cuenca_validations.types import (
    BatchFileMetadata,
    FileBatchUploadRequest,
    FileRequest,
)

from ..http import Session, session as global_session
from .base import Creatable, Queryable


class FileBatch(Creatable, Queryable):
    _resource: ClassVar = 'file_batches'

    received_files: list[BatchFileMetadata]
    uploaded_files: list[BatchFileMetadata]
    user_id: str

    @classmethod
    def create(
        cls,
        files: list[dict],
        user_id: str,
        *,
        session: Session = global_session,
    ) -> 'FileBatch':
        req = FileBatchUploadRequest(
            files=[FileRequest(**f) for f in files],
            user_id=user_id,
        )
        return cls._create(session=session, **req.model_dump())
