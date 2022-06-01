from typing import ClassVar

from cuenca_validations.types import StatementQuery

from .base import Downloadable, Queryable


class Statement(Queryable, Downloadable):
    _resource: ClassVar = 'statements'
    _query_params: ClassVar = StatementQuery

    month: int
    year: int
