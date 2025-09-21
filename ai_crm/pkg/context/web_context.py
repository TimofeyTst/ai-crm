from fastapi import Request

from ai_crm.pkg.connectors.postgresql import resource as PostgreSQLResource
from ai_crm.pkg.logger import logger as logger_lib

logger = logger_lib.get_logger(__name__)


class WebContext:
    """Web context that manages application resources and lifecycle."""
    
    def __init__(self):
        self.postgresql = PostgreSQLResource.Resource()
        logger.info("WebContext initialized")
    
    async def on_startup(self) -> None:
        """Initialize all resources on startup."""
        logger.info("Starting up WebContext...")

        await self.postgresql.on_startup()

        logger.info("WebContext startup completed")
    
    async def on_shutdown(self) -> None:
        """Cleanup all resources on shutdown."""
        logger.info("Shutting down WebContext...")

        await self.postgresql.on_shutdown()

        logger.info("WebContext shutdown completed")

def get_web_context_dependency():
    """Dependency function to get WebContext from FastAPI app state."""
    def _get_web_context(request: Request):
        return getattr(request.app.state, 'web_context')

    return _get_web_context
