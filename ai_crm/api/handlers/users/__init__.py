from starlette import status
from fastapi import APIRouter, Depends

from ai_crm.api.middlewares import token_based_verification as auth
from ai_crm.pkg.models.exceptions import users
from ai_crm.api.handlers.users import users_get_v1
from ai_crm.pkg.context import web_context

user_router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={
        **users.UserNotFound.generate_openapi(),
        **users.DuplicateUserName.generate_openapi(),
    },
)

@user_router.get(
    "/v1",
    status_code=status.HTTP_200_OK,
    description="Get all users",
    dependencies=[Depends(auth.token_based_verification)],
)
async def _users_get_v1(web_context: web_context.WebContext = Depends(web_context.get_web_context_dependency())):
    return await users_get_v1.handle(web_context)

