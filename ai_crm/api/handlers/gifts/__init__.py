from starlette import status
from fastapi import APIRouter, Depends, Path

from ai_crm.api.middlewares import token_based_verification as auth
from ai_crm.api.handlers.gifts import gifts_get_v1, gifts_create_v1, gifts_update_v1, gifts_delete_v1, gifts_get_by_id_v1
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

@gift_router.get(
    "/v1/{gift_id}",
    status_code=status.HTTP_200_OK,
    description="Get gift by ID",
    response_model=gift_models.Gift,
    dependencies=[Depends(auth.token_based_verification)],
)
async def _gifts_get_by_id_v1(
    gift_id: str = Path(..., description="Gift ID"),
    web_context: web_context.WebContext = Depends(web_context.get_web_context_dependency())
):
    return await gifts_get_by_id_v1.handle(web_context, gift_id)

@gift_router.post(
    "/v1/create",
    status_code=status.HTTP_201_CREATED,
    description="Create new gift",
    response_model=gift_models.Gift,
    dependencies=[Depends(auth.token_based_verification)],
)
async def _gifts_create_v1(
    request: gift_models.GiftCreateRequest,
    web_context: web_context.WebContext = Depends(web_context.get_web_context_dependency())
):
    return await gifts_create_v1.handle(web_context, request)

@gift_router.post(
    "/v1/update",
    status_code=status.HTTP_200_OK,
    description="Update gift",
    response_model=gift_models.Gift,
    dependencies=[Depends(auth.token_based_verification)],
)
async def _gifts_update_v1(
    request: gift_models.GiftUpdateRequest,
    web_context: web_context.WebContext = Depends(web_context.get_web_context_dependency())
):
    return await gifts_update_v1.handle(web_context, request)

@gift_router.post(
    "/v1/delete",
    status_code=status.HTTP_200_OK,
    description="Delete gift",
    dependencies=[Depends(auth.token_based_verification)],
)
async def _gifts_delete_v1(
    request: gift_models.GiftDeleteRequest,
    web_context: web_context.WebContext = Depends(web_context.get_web_context_dependency())
):
    return await gifts_delete_v1.handle(web_context, request)
