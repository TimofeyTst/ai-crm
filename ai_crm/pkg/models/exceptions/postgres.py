
from starlette import status

from ai_crm.pkg.models.base import exception as base_exceptions

class EmptyResult(base_exceptions.BaseAPIException):
    error_code = 'empty_result'
    error_msg = 'Empty result.'
    http_code = status.HTTP_404_NOT_FOUND
