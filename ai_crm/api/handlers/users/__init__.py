from starlette import status
from fastapi import APIRouter, Depends

from ai_crm.api.middlewares import token_based_verification as auth
from ai_crm.pkg.models.exceptions import users
from ai_crm.api.handlers.users import users_get_v1, users_create_v1
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import user as user_models

user_router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={
        **users.UserNotFound.generate_openapi(),
        **users.UserAlreadyExists.generate_openapi(),
    },
)

@user_router.get(
    "/v1",
    status_code=status.HTTP_200_OK,
    description="Get all users",
    response_model=list[user_models.User],
    dependencies=[Depends(auth.token_based_verification)],
)
async def _users_get_v1(web_context: web_context.WebContext = Depends(web_context.get_web_context_dependency())):
    return await users_get_v1.handle(web_context)

@user_router.post(
    "/v1/create",
    status_code=status.HTTP_201_CREATED,
    description="Create new user",
    response_model=user_models.User,
    dependencies=[Depends(auth.token_based_verification)],
)
async def _users_create_v1(
    request: user_models.UserCreateRequest,
    web_context: web_context.WebContext = Depends(web_context.get_web_context_dependency())
):
    return await users_create_v1.handle(web_context, request)

