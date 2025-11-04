from fastapi import APIRouter, Depends
from starlette import status

from ai_crm.api.handlers.auth import (
    auth_login_v1,
    auth_refresh_v1,
    auth_register_v1,
)
from ai_crm.api.middlewares import jwt_auth
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import auth as auth_models
from ai_crm.pkg.models.ai_crm import user as user_models
from ai_crm.pkg.models.exceptions import auth as auth_exceptions
from ai_crm.pkg.models.exceptions import users as users_exceptions

auth_router = APIRouter(
    prefix="/v1/auth",
    tags=["Auth"],
    responses={
        **auth_exceptions.InvalidCredentials.generate_openapi(),
        **auth_exceptions.InvalidToken.generate_openapi(),
        **users_exceptions.UserAlreadyExists.generate_openapi(),
    },
)


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    description="Register a new user",
    response_model=auth_models.TokenResponse,
)
async def _auth_register_v1(
    request: auth_models.RegisterRequest,
    web_context: web_context.WebContext = Depends(
        web_context.get_web_context_dependency()
    ),
):
    return await auth_register_v1.handle(web_context, request)


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    description="Login user and get JWT tokens",
    response_model=auth_models.TokenResponse,
)
async def _auth_login_v1(
    request: auth_models.LoginRequest,
    web_context: web_context.WebContext = Depends(
        web_context.get_web_context_dependency()
    ),
):
    return await auth_login_v1.handle(web_context, request)


@auth_router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    description="Refresh access token using refresh token",
    response_model=auth_models.TokenResponse,
)
async def _auth_refresh_v1(
    request: auth_models.RefreshTokenRequest,
    web_context: web_context.WebContext = Depends(
        web_context.get_web_context_dependency()
    ),
):
    return await auth_refresh_v1.handle(web_context, request)


@auth_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    description="Get current authenticated user",
    response_model=user_models.User,
)
async def _auth_me_v1(
    current_user: user_models.User = Depends(jwt_auth.get_current_user),
):
    return current_user


# TODO: logout + redis
