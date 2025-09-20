from starlette.responses import JSONResponse

from ai_crm.internal.services import users as users_service
from ai_crm.pkg.context import web_context
from fastapi import status

async def handle(context: web_context.WebContext):
    users = await users_service.get_users(context)
    users_dict = [user.to_json_dict() for user in users]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "AI CRM OK USERS GET V1", "users": users_dict},
    )
