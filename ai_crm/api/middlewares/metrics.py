"""Middleware for expose internal metrics to public endpoint."""

# TODO prometheus
# from prometheus_client.openmetrics.exposition import (
#     CONTENT_TYPE_LATEST,
#     generate_latest,
# )
# from prometheus_client.registry import REGISTRY
from starlette.requests import Request
from starlette.responses import Response

from ai_crm.pkg.logger import logger as logger_lib

logger = logger_lib.get_logger(__name__)


def metrics(request: Request) -> Response:
    """Expose internal metrics to public endpoint.

    Args:
        request:
            ``Request`` instance.

    Returns:
        ``Response`` instance with metrics.
    """

    del request  # unused

    logger.error(f"METRICS NOT SETTED!")

    return Response(
        # generate_latest(REGISTRY),
        # headers={"Content-Type": CONTENT_TYPE_LATEST},
    )
