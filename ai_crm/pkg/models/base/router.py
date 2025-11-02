from dataclasses import dataclass

from fastapi import APIRouter, FastAPI


@dataclass(frozen=True)
class Router:
    routers: tuple[APIRouter, ...]

    def register_routes(self, app: FastAPI):
        for router in self.routers:
            app.include_router(router)
