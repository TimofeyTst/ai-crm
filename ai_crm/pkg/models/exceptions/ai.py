from ai_crm.pkg.models.base import exception as base_exceptions


class ResumeParsingFailed(base_exceptions.BaseAPIException):
    error_code = "resume_parsing_failed"
    error_msg = "Failed to parse resume content"
    http_code = 422


class ResumePersonalizationFailed(base_exceptions.BaseAPIException):
    error_code = "resume_personalization_failed"
    error_msg = "Failed to personalize resume"
    http_code = 500


class ResumeGenerationFailed(base_exceptions.BaseAPIException):
    error_code = "resume_generation_failed"
    error_msg = "Failed to generate resume document"
    http_code = 500


class OpenAIAPIError(base_exceptions.BaseAPIException):
    error_code = "openai_api_error"
    error_msg = "OpenAI API request failed"
    http_code = 503
