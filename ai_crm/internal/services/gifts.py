from ai_crm.internal.repository.postgresql import gifts as gifts_repository
from ai_crm.pkg.models.ai_crm import gift as gift_models
from ai_crm.pkg import context

async def get_gifts(context: context.AnyContext) -> list[gift_models.Gift]:
    return await gifts_repository.get_gifts(context)

async def get_gift_by_id(context: context.AnyContext, gift_id: int) -> gift_models.Gift:
    return await gifts_repository.get_gift_by_id(context, gift_id)

async def create_gift(context: context.AnyContext, request: gift_models.GiftCreateRequest) -> gift_models.Gift:
    return await gifts_repository.create_gift(context, request)

async def update_gift(context: context.AnyContext, request: gift_models.GiftUpdateRequest) -> gift_models.Gift:
    return await gifts_repository.update_gift(context, request)

async def delete_gift(context: context.AnyContext, request: gift_models.GiftDeleteRequest) -> None:
    return await gifts_repository.delete_gift(context, request)
