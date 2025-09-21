from ai_crm.internal.services import gifts as gifts_service
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import gift as gift_models

async def handle(context: web_context.WebContext, request: gift_models.GiftCreateRequest) -> gift_models.Gift:
    return await gifts_service.create_gift(context, request)
