from starlette import status

from ai_crm.pkg.models.base import exception as base_exceptions


class ResumeNotFound(base_exceptions.BaseAPIException):
    error_code = "resume_not_found"
    error_msg = "Resume not found."
    http_code = status.HTTP_404_NOT_FOUND


class ResumeAccessDenied(base_exceptions.BaseAPIException):
    error_code = "resume_access_denied"
    error_msg = "Access to this resume is denied."
    http_code = status.HTTP_403_FORBIDDEN


class InvalidFileType(base_exceptions.BaseAPIException):
    error_code = "invalid_file_type"
    error_msg = "Invalid file type. Only PDF files are allowed."
    http_code = status.HTTP_400_BAD_REQUEST


class FileTooLarge(base_exceptions.BaseAPIException):
    error_code = "file_too_large"
    error_msg = "File size exceeds maximum allowed size (10 MB)."
    http_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


class FileNotFoundInStorage(base_exceptions.BaseAPIException):
    error_code = "file_not_found_in_storage"
    error_msg = "File not found in storage."
    http_code = status.HTTP_404_NOT_FOUND
