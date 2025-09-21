from ai_crm.pkg.connectors.postgresql import psql
from ai_crm.internal.repository.postgresql.collect_response import collect_response
from ai_crm.pkg.models.ai_crm import user as user_models
from ai_crm.pkg import context

@collect_response  
async def get_users_as_models(context: context.AnyContext) -> list[user_models.User]:
    async with psql.get_connection(context, read_only=True) as conn:
        print(f"YC version: {await conn.fetch('SELECT version()')}")
        return await conn.fetch("SELECT * FROM users")
