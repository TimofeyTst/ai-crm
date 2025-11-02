from fastapi import FastAPI

from ai_crm.api.server import Server


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api")
    return Server(app).get_app()
