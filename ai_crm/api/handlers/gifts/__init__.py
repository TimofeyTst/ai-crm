from starlette import status
from fastapi import APIRouter, Depends

from ai_crm.api.middlewares import token_based_verification as auth
from ai_crm.api.handlers.gifts import gifts_get_v1
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import gift as gift_models

gift_router = APIRouter(
    prefix="/gifts",
    tags=["Gift"],
)

@gift_router.get(
    "/v1",
    status_code=status.HTTP_200_OK,
    description="Get all gifts",
    response_model=list[gift_models.Gift],
    dependencies=[Depends(auth.token_based_verification)],
)
async def _gifts_get_v1(web_context: web_context.WebContext = Depends(web_context.get_web_context_dependency())):
    return await gifts_get_v1.handle(web_context)
