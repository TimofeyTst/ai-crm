from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from ai_crm.pkg.logger import logger as logger_lib
from ai_crm.pkg.models.base import exception as base_exceptions

logger = logger_lib.get_logger(__name__)


def handle_api_exceptions(
    request: Request, exc: base_exceptions.BaseAPIException
):
    """Handle all internal exceptions that inherited from
    :class:`.base_exceptions.BaseAPIException`.

    Args:
        request:
            ``Request`` instance.
        exc:
            Exception inherited from :class:`.base_exceptions.BaseAPIException`.

    Returns:
        ``JSONResponse`` object with status code from ``exc.status_code``.
    """

    del request  # unused

    logger.info(f"api exception: {str(type(exc))}: {exc}")

    return JSONResponse(
        status_code=exc.http_code, content={"message": exc.error_msg}
    )


def handle_internal_exception(request: Request, exc: Exception):
    """Handle all internal unhandled exceptions.

    Args:
        request:
            ``Request`` instance.
        exc:
            ``Exception`` instance.

    Returns:
        ``JSONResponse`` object with status code 500.
    """

    del request  # unused

    logger.exception(f"internal exception: {str(type(exc))}: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(exc)},
    )
