class CuencaException(Exception):
    ...


class NoResultFound(CuencaException):
    ...


class MultipleResultsFound(CuencaException):
    ...
