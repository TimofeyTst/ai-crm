from ai_crm.internal.repository.postgresql import users as users_repository
from ai_crm.pkg import context

async def get_users(context: context.AnyContext):
    return await users_repository.get_users_as_models(context)
