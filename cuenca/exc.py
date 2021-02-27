from dataclasses import dataclass

from cuenca_validations.typing import DictStrAny


class CuencaException(Exception):
    ...


class MalformedJwtToken(CuencaException):
    """An invalid JWT token was obtained during authentication"""


class NoResultFound(CuencaException):
    """No results were found"""


class MultipleResultsFound(CuencaException):
    """One result was expected but multiple were returned"""


@dataclass
class CuencaResponseException(CuencaException):
    json: DictStrAny
    status_code: int

    def __str__(self) -> str:
        return repr(self)


class InvalidPassword(CuencaResponseException):
    """Unable to authenticate with the provided password"""


class NoPasswordFound(CuencaResponseException):
    """User must create a password before to continue"""


class UserNotLoggedIn(CuencaResponseException):
    """Login required for this method"""
