
from starlette import status

from ai_crm.pkg.models.base import exception as base_exceptions

class UserNotFound(base_exceptions.BaseAPIException):
    error_code = 'user_not_found'
    error_msg = 'User not found.'
    http_code = status.HTTP_404_NOT_FOUND


class UserAlreadyExists(base_exceptions.BaseAPIException):
    error_code = 'user_already_exists'
    error_msg = 'User with this email or username already exists.'
    http_code = status.HTTP_409_CONFLICT


class InactiveUser(base_exceptions.BaseAPIException):
    error_code = 'inactive_user'
    error_msg = 'User account is inactive.'
    http_code = status.HTTP_403_FORBIDDEN

__constrains__ = {
    "user_code_key": UserAlreadyExists,
}
