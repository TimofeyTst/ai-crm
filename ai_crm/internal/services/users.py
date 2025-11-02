from ai_crm.internal.repository.postgresql import users as users_repository
from ai_crm.pkg import context
from ai_crm.pkg.models.ai_crm import user as user_models
from ai_crm.pkg.models.exceptions import users as users_exceptions, postgres as postgres_exceptons

async def get_users(context: context.AnyContext) -> list[user_models.User]:
    return await users_repository.get_users_as_models(context)


async def create_user(context: context.AnyContext, request: user_models.UserCreateRequest) -> user_models.User:
    return await users_repository.create_user(context, request)


async def get_user_by_user_id(context: context.AnyContext, user_id: str) -> user_models.User:
    try:
        user = await users_repository.get_user_by_id(context, user_id)
    except postgres_exceptons.EmptyResult:
        raise users_exceptions.UserNotFound
    
    if not user.is_active:
        raise users_exceptions.InactiveUser

    return user


async def get_user_by_email(context: context.AnyContext, email: str) -> user_models.User:
    try:
        user = await users_repository.get_user_by_email(context, email)
    except postgres_exceptons.EmptyResult:
        raise users_exceptions.UserNotFound
    
    if not user.is_active:
        raise users_exceptions.InactiveUser

    return user
