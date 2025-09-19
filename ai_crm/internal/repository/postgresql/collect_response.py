from functools import wraps
from typing import List, Type, Union

import asyncpg
import pydantic

from ai_crm.pkg.models.base import model as base_models
from ai_crm.pkg.models.exceptions import postgres as postgres_exceptions


def collect_response(fn):
    """Convert response from asyncpg to an annotated model.

    Args:
        fn:
            Target function that contains a query in postgresql.

    Examples:
        If you have a function that contains a query in postgresql,
        decorator :func:`.collect_response` will convert the response from asyncpg to
        an annotated model::

            >>> from ai_crm.pkg.models.user import StrictUser, ReadUserByIdQuery
            >>> from ai_crm.pkg.connectors import psql
            >>>
            >>> @collect_response
            ... async def get_user_by_id(query: ReadUserByIdQuery) -> StrictUser:
            ...    q = "SELECT * FROM users WHERE id = $1"
            ...    async with psql.get_connection() as conn:
            ...        return await conn.fetchrow(q, query.id)

    Warnings:
        The function must return a single asyncpg.Record or a list of asyncpg.Record objects.

    Returns:
        The model that is specified in type hints of `fn`.

    Raises:
        EmptyResult: when a query of `fn` returns None.
    """

    @wraps(fn)
    async def inner(
        *args: object,
        **kwargs: object,
    ) -> Union[List[Type[base_models.BaseModel]], Type[base_models.BaseModel]]:
        response = await fn(*args, **kwargs)
        if not response:
            raise postgres_exceptions.EmptyResult

        # Get return type annotation
        return_annotation = fn.__annotations__["return"]
        
        # Create TypeAdapter for Pydantic v2
        type_adapter = pydantic.TypeAdapter(return_annotation)
        
        # Convert response and validate with Pydantic v2
        converted_response = await __convert_response(response=response, annotations=str(return_annotation))
        return type_adapter.validate_python(converted_response)

    return inner


async def __convert_response(response: Union[asyncpg.Record, List[asyncpg.Record]], annotations: str):
    if annotations.startswith("list"):
        return [dict(record) for record in response]
    else:
        return dict(response)


