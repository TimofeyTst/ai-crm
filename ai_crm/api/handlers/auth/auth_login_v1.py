from ai_crm.internal.services import auth as auth_service
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import auth as auth_models


async def handle(
    context: web_context.WebContext,
    request: auth_models.LoginRequest
) -> auth_models.TokenResponse:
    return await auth_service.login(context, request)

