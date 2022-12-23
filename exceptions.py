class CheckOutProjectException(Exception):
    """Base Exception for project."""


class HTTPException(CheckOutProjectException):
    """Exception while getting HTTP response."""
