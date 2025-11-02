from ai_crm.internal.repository.postgresql.collect_response import (
    collect_response,
)
from ai_crm.pkg import context
from ai_crm.pkg.connectors.postgresql import psql
from ai_crm.pkg.models.ai_crm import gift as gift_models
from ai_crm.pkg.models.consts import postgres as psql_consts
from ai_crm.pkg.models.exceptions import postgres as psql_exceptions


@collect_response
async def get_gifts(context: context.AnyContext) -> list[gift_models.Gift]:
    async with psql.get_connection(context, read_only=True) as conn:
        return await conn.fetch("SELECT * FROM gifts")


@collect_response
async def get_gift_by_id(
    context: context.AnyContext, gift_id: int
) -> gift_models.Gift:
    async with psql.get_connection(context, read_only=True) as conn:
        rows = await conn.fetch(
            "SELECT * FROM gifts WHERE gift_id = $1", gift_id
        )
        if not rows or len(rows) != 1:
            raise psql_exceptions.EmptyResult(
                f"Gift with id {gift_id} not found"
            )

        return rows[0]


@collect_response
async def create_gift(
    context: context.AnyContext, request: gift_models.GiftCreateRequest
) -> gift_models.Gift:
    async with psql.get_connection(context) as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO gifts (gift_id, price, total_count, remaining_count, is_limited)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
            """,
            request.gift_id,
            request.price,
            request.total_count,
            request.remaining_count,
            request.is_limited,
        )
        return row


@collect_response
async def update_gift(
    context: context.AnyContext, request: gift_models.GiftUpdateRequest
) -> gift_models.Gift:
    async with psql.get_connection(context) as conn:
        fields_to_update = []
        params = []
        param_count = 1

        if request.price is not None:
            fields_to_update.append(f"price = ${param_count}")
            params.append(request.price)
            param_count += 1

        if request.total_count is not None:
            fields_to_update.append(f"total_count = ${param_count}")
            params.append(request.total_count)
            param_count += 1

        if request.remaining_count is not None:
            fields_to_update.append(f"remaining_count = ${param_count}")
            params.append(request.remaining_count)
            param_count += 1

        if request.is_limited is not None:
            fields_to_update.append(f"is_limited = ${param_count}")
            params.append(request.is_limited)
            param_count += 1

        if not fields_to_update:
            # If no fields to update, just return the existing gift
            return await get_gift_by_id(context, request.gift_id)

        params.append(request.gift_id)  # For WHERE clause

        query = f"""
        UPDATE gifts
        SET {', '.join(fields_to_update)}
        WHERE gift_id = ${param_count}
        RETURNING *
        """

        row = await conn.fetchrow(query, *params)
        if not row:
            raise psql_exceptions.EmptyResult(
                f"Gift with id {request.gift_id} not found"
            )
        return row


async def delete_gift(
    context: context.AnyContext, request: gift_models.GiftDeleteRequest
) -> None:
    async with psql.get_connection(context) as conn:
        result = await conn.execute(
            "DELETE FROM gifts WHERE gift_id = $1", request.gift_id
        )
        if result == psql_consts.DELETE_ZERO:
            raise psql_exceptions.EmptyResult(
                f"Gift with id {request.gift_id} not found"
            )
