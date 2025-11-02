from ai_crm.internal.services import users as users_service
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import user as user_models


async def handle(
    context: web_context.WebContext, request: user_models.UserCreateRequest
) -> user_models.User:
    return await users_service.create_user(context, request)
