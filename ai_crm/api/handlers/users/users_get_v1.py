from starlette.responses import JSONResponse

from ai_crm.internal.services import users as users_service
from fastapi import status

async def handle():
    users = await users_service.get_users()
    users_dict = [user.to_json_dict() for user in users]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "AI CRM OK USERS GET V1", "users": users_dict},
    )
