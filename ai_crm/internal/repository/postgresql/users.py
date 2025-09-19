from ai_crm.pkg.connectors import psql
from ai_crm.internal.repository.postgresql.collect_response import collect_response
from ai_crm.pkg.models.ai_crm import user as user_models

@collect_response  
async def get_users_as_models() -> list[user_models.User]:
    async with psql.get_connection() as conn:
        return await conn.fetch("SELECT * FROM users")
