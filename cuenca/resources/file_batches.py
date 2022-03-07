from typing import ClassVar, Dict, List, cast

from cuenca_validations.types import BatchFileMetadata, FileBatchUploadRequest
from pydantic.dataclasses import dataclass

from ..http import Session, session as global_session
from .base import Creatable, Queryable


@dataclass
class FileBatch(Creatable, Queryable):
    _resource: ClassVar = 'file_batches'

    received_files: List[BatchFileMetadata]
    uploaded_files: List[BatchFileMetadata]
    user_id: str

    @classmethod
    def create(
        cls,
        files: List[Dict],
        user_id: str,
        *,
        session: Session = global_session,
    ) -> 'FileBatch':
        req = FileBatchUploadRequest(files=files, user_id=user_id)
        return cast('FileBatch', cls._create(session=session, **req.dict()))
