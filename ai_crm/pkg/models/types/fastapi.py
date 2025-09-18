from typing import TypeVar

from fastapi import FastAPI

instance = TypeVar("instance", bound=FastAPI)
