from starlette import status
from starlette.responses import JSONResponse

from ai_crm.internal.services import gifts as gifts_service
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import gift as gift_models


async def handle(
    context: web_context.WebContext, request: gift_models.GiftDeleteRequest
) -> JSONResponse:
    await gifts_service.delete_gift(context, request)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Gift deleted successfully"},
    )
