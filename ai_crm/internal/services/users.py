from ai_crm.internal.repository.postgresql import users as users_repository
from ai_crm.pkg import context
from ai_crm.pkg.models.ai_crm import user as user_models

async def get_users(context: context.AnyContext) -> list[user_models.User]:
    return await users_repository.get_users_as_models(context)

async def create_user(context: context.AnyContext, request: user_models.UserCreateRequest) -> user_models.User:
    return await users_repository.create_user(context, request)
