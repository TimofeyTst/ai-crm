from starlette import status

from ai_crm.pkg.models.base import exception as base_exceptions


class InvalidCredentials(base_exceptions.BaseAPIException):
    error_code = "invalid_credentials"
    error_msg = "Could not validate credentials."
    http_code = status.HTTP_403_FORBIDDEN
