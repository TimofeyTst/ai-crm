from ai_crm.pkg.connectors.postgresql import psql
from ai_crm.internal.repository.postgresql.collect_response import collect_response
from ai_crm.pkg.models.ai_crm import gift as gift_models
from ai_crm.pkg import context

@collect_response  
async def get_gifts(context: context.AnyContext) -> list[gift_models.Gift]:
    async with psql.get_connection(context, read_only=True) as conn:
        return await conn.fetch("SELECT * FROM gifts")
