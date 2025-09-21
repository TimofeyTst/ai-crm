from ai_crm.internal.repository.postgresql import gifts as gifts_repository
from ai_crm.pkg.models.ai_crm import gift as gift_models
from ai_crm.pkg import context

async def get_gifts(context: context.AnyContext) -> list[gift_models.Gift]:
    return await gifts_repository.get_gifts(context)
