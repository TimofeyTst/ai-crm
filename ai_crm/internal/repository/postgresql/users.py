from ai_crm.pkg.connectors.postgresql import psql
from ai_crm.internal.repository.postgresql.collect_response import collect_response
from ai_crm.pkg.models.ai_crm import user as user_models
from ai_crm.pkg import context
from ai_crm.pkg.models.exceptions import postgres as psql_exceptions

@collect_response  
async def get_users_as_models(context: context.AnyContext) -> list[user_models.User]:
    async with psql.get_connection(context, read_only=True) as conn:
        return await conn.fetch("SELECT * FROM users")

@collect_response
async def create_user(context: context.AnyContext, request: user_models.UserCreateRequest) -> user_models.User:
    async with psql.get_connection(context) as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO users (username, email, password_hash, first_name, last_name, is_active)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *
            """,
            request.username,
            request.email,
            request.password_hash,
            request.first_name,
            request.last_name,
            request.is_active
        )
        return row
