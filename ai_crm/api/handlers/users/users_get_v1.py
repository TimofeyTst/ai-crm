from starlette.responses import JSONResponse

from fastapi import status

async def handle():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "AI CRM OK USERS GET V1"},
    )
