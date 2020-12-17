from typing import ClassVar

from cuenca_validations.types import FileFormat, StatementQuery
from pydantic.dataclasses import dataclass

from .base import Downloadable, Queryable


@dataclass
class Statement(Queryable, Downloadable):
    _resource: ClassVar = 'statements'
    _query_params: ClassVar = StatementQuery

    month: int
    year: int

    @property
    def pdf(self) -> bytes:
        return self.download(self.id, file_format=FileFormat.pdf).read()

    @property
    def xml(self) -> bytes:
        return self.download(self.id, file_format=FileFormat.xml).read()
