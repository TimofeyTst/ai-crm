"""Authentication service."""

from ai_crm.internal.repository.postgresql import users as users_repository
from ai_crm.internal.services import users as users_lib
from ai_crm.pkg import context
from ai_crm.pkg.configuration import settings
from ai_crm.pkg.logger import logger as logger_lib
from ai_crm.pkg.models.ai_crm import auth as auth_models
from ai_crm.pkg.models.ai_crm import user as user_models
from ai_crm.pkg.models.exceptions import auth as auth_exceptions
from ai_crm.pkg.models.exceptions import postgres as postgres_exceptons
from ai_crm.pkg.models.exceptions import users as users_excpetions
from ai_crm.pkg.utils import jwt as jwt_utils
from ai_crm.pkg.utils import password as password_utils

logger = logger_lib.get_logger(__name__)


async def register(
    context: context.AnyContext, request: auth_models.RegisterRequest
) -> auth_models.TokenResponse:
    # TODO: create psql index and assert on index if this email/username already exist
    try:
        await users_repository.get_user_by_email(context, request.email)
        await users_repository.get_user_by_username(context, request.username)
        raise users_excpetions.UserAlreadyExists
    except postgres_exceptons.EmptyResult:
        pass

    hashed_password = password_utils.hash_password(request.password)

    logger.info(
        f"Password hashed successfully for username: {request.username}, hash length: {len(hashed_password)}"
    )

    create_request = user_models.UserCreateRequest(
        username=request.username,
        email=request.email,
        password_hash=hashed_password,
        first_name=request.first_name,
        last_name=request.last_name,
        is_active=True,
    )

    user = await users_lib.create_user(context, create_request)
    return _create_tokens(user)


async def login(
    context: context.AnyContext, request: auth_models.LoginRequest
) -> auth_models.TokenResponse:
    user = await users_lib.get_user_by_email(context, request.email)

    if not password_utils.verify_password(request.password, user.password_hash):
        raise auth_exceptions.InvalidCredentials

    return _create_tokens(user)


async def refresh(
    context: context.AnyContext, refresh_token: str
) -> auth_models.TokenResponse:
    user = await _get_user_from_jwt(
        context, refresh_token, token_type="refresh"
    )
    return _create_tokens(user)


async def get_current_user(
    context: context.AnyContext, token: str
) -> user_models.User:
    return await _get_user_from_jwt(context, token, token_type="access")


async def _get_user_from_jwt(
    context: context.AnyContext,
    token: str,
    token_type: str,
) -> user_models.User:
    """Validate jwt and get user"""
    payload = jwt_utils.decode_token(token, token_type=token_type)
    if not payload:
        raise auth_exceptions.InvalidToken

    user_id = payload.get("sub")
    return await users_lib.get_user_by_user_id(context, user_id)


def _create_tokens(user: user_models.User) -> auth_models.TokenResponse:
    token_data = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
    }

    access_token = jwt_utils.create_access_token(data=token_data)
    refresh_token = jwt_utils.create_refresh_token(data=token_data)

    return auth_models.TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ai_crm_env.API.REFRESH_TOKEN_EXPIRE_SECONDS,
    )
