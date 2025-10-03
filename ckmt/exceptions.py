"""Exception classes for CKMT SDK"""


class CKMTError(Exception):
    """Base exception for all CKMT errors"""
    pass


class APIError(CKMTError):
    """Raised when the API returns an error"""

    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class AuthenticationError(APIError):
    """Raised when authentication fails"""
    pass


class RateLimitError(APIError):
    """Raised when rate limit is exceeded"""
    pass


class NotFoundError(APIError):
    """Raised when a resource is not found"""
    pass


class ValidationError(APIError):
    """Raised when request validation fails"""
    pass
