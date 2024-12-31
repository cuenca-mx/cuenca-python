from cuenca_validations.typing import DictStrAny


class CuencaException(Exception):
    """Base Exception Class"""


class MalformedJwtToken(CuencaException):
    """An invalid JWT token was obtained during authentication"""


class NoResultFound(CuencaException):
    """No results were found"""


class MultipleResultsFound(CuencaException):
    """One result was expected but multiple were returned"""


class CuencaResponseException(CuencaException):
    def __init__(self, json: DictStrAny, status_code: int) -> None:
        self.json = json
        self.status_code = status_code
        super().__init__()

    def __str__(self) -> str:
        return repr(self)
