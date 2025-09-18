
from starlette import status

from ai_crm.pkg.models.base import exception as base_exceptions

class UserNotFound(base_exceptions.BaseAPIException):
    error_code = 'user_not_found'
    error_msg = 'User not found.'
    http_code = status.HTTP_404_NOT_FOUND


class DuplicateUserName(base_exceptions.BaseAPIException):
    error_code = 'duplicate_user_name'
    error_msg = 'User name already exists.'
    http_code = status.HTTP_409_CONFLICT


__constrains__ = {
    "user_code_key": DuplicateUserName,
}
