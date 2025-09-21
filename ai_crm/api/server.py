"""Server configuration."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_crm.api.logger import EndpointFilter
from ai_crm.api.middlewares import handle_http_exceptions
from ai_crm.api.middlewares import metrics
from ai_crm.api.middlewares import prometheus
from ai_crm.api import handlers
from ai_crm.pkg.models.base import exception as base_exception
from ai_crm.pkg.models.types import fastapi
from ai_crm.pkg.configuration import settings
from ai_crm.pkg.context.web_context import WebContext

class Server:
    """Register all requirements for the correct work of server instance.

    Attributes:
        __app:
            ``FastAPI`` application instance.
        __app_name:
            Name of application used for prometheus metrics and for loki logs.
            Getting from :class:`.Settings`:attr:`.INSTANCE_APP_NAME`.
    """

    __app: FastAPI
    __app_name: str = settings.ai_crm_env.INSTANCE_APP_NAME
    __web_context: WebContext

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__web_context = WebContext()
        # Store web_context in app state for access in handlers
        app.state.web_context = self.__web_context
        
        self._register_routes(app)
        self._register_middlewares(app)
        self._register_http_exceptions(app)
        self._register_events(app)

    def get_app(self) -> FastAPI:
        return self.__app

    @staticmethod
    def _register_routes(app: fastapi.instance) -> None:
        handlers.__router__.register_routes(app)

    def _register_events(self, app: fastapi.instance) -> None:
        app.on_event("startup")(self.__web_context.on_startup)
        app.on_event("shutdown")(self.__web_context.on_shutdown)

    def _register_middlewares(self, app: fastapi.instance) -> None:
        self.__register_cors_origins(app)
        self.__register_prometheus(app)

    @staticmethod
    def _register_http_exceptions(app: fastapi.instance) -> None:
        app.add_exception_handler(base_exception.BaseAPIException, handle_http_exceptions.handle_api_exceptions)
        app.add_exception_handler(Exception, handle_http_exceptions.handle_internal_exception)

    @staticmethod
    def __register_cors_origins(app: fastapi.instance) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def __register_prometheus(self, app: fastapi.instance) -> None:
        app.add_middleware(
            prometheus.PrometheusMiddleware,
            app_name=self.__app_name,
        )

        self.__register_metrics_collector(app)

    def __register_metrics_collector(
        self,
        app: fastapi.instance,
    ) -> None:
        metrics_endpoint = "/metrics"
        app.add_route(metrics_endpoint, metrics.metrics)
        self.__filter_logs(metrics_endpoint)

    @staticmethod
    def __filter_logs(endpoint: str) -> None:
        logging.getLogger("uvicorn.access").addFilter(EndpointFilter(endpoint=endpoint))
