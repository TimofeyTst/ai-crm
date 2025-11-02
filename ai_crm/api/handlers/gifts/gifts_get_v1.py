from ai_crm.internal.services import gifts as gifts_service
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import gift as gift_models


async def handle(context: web_context.WebContext) -> list[gift_models.Gift]:
    return await gifts_service.get_gifts(context)
