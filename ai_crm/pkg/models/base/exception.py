from starlette import status

class BaseError(Exception):
    error_code = 'internal_error'
    error_msg = 'Unhandled exception'
    http_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, error_code=None, error_msg=None, details=None):
        super().__init__(error_msg)
        if error_code:
            self.error_code = error_code
        if error_msg:
            self.error_msg = error_msg
        self.details = details

    def __str__(self):
        base_str = f'{self.__class__.__name__}[{self.http_code}]({self.error_code}): {self.error_msg}'

        if self.details:
            return f'{base_str}<{self.details}>'

        return base_str


class BaseAPIException(BaseError):
    @classmethod
    def generate_openapi(cls):
        return {
            cls.http_code: {
                "description": cls.error_msg,
                "content": {
                    "application/json": {
                        "example": {
                            "message": cls.error_msg,
                        },
                    },
                },
            },
        }
