from ai_crm.internal.repository.postgresql import users as users_repository

async def get_users():
    return await users_repository.get_users_as_models()
