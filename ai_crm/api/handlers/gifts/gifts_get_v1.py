from ai_crm.internal.services import gifts as gifts_service
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import gift as gift_models

async def handle(context: web_context.WebContext) -> list[gift_models.Gift]:
    gifts = await gifts_service.get_gifts(context)
    # users_dict = [user.to_json_dict() for user in users]

    return gifts
