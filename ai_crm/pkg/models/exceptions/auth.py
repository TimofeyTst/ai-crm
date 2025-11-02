from starlette import status

from ai_crm.pkg.models.base import exception as base_exceptions


class InvalidCredentials(base_exceptions.BaseAPIException):
    error_code = 'invalid_credentials'
    error_msg = 'Invalid email or password.'
    http_code = status.HTTP_401_UNAUTHORIZED


class InvalidToken(base_exceptions.BaseAPIException):
    error_code = 'invalid_token'
    error_msg = 'Invalid or expired token.'
    http_code = status.HTTP_401_UNAUTHORIZED
