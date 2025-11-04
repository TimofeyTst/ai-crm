from pydantic.fields import Field

from ai_crm.pkg.models.base import model as base_models


class GiftFields:
    gift_id: str = Field(description="Gift id.", example=1)
    price: int = Field(description="Gift price.", example=100)
    total_count: int = Field(description="Gift total count.", example=100)
    remaining_count: int = Field(
        description="Gift remaining count.", example=100
    )
    is_limited: bool = Field(description="Gift is limited.", example=True)


class Gift(base_models.BaseModel):
    gift_id: str = GiftFields.gift_id
    price: int = GiftFields.price
    total_count: int | None = GiftFields.total_count
    remaining_count: int | None = GiftFields.remaining_count
    is_limited: bool = GiftFields.is_limited


# Requests or commands
class GiftCreateRequest(Gift):
    pass


class GiftUpdateRequest(Gift):
    gift_id: str = GiftFields.gift_id
    price: int | None = Field(None, description="Gift price.", example=100)
    total_count: int | None = Field(
        None, description="Gift total count.", example=100
    )
    remaining_count: int | None = Field(
        None, description="Gift remaining count.", example=100
    )
    is_limited: bool | None = Field(
        None, description="Gift is limited.", example=True
    )


class GiftDeleteRequest(base_models.BaseModel):
    gift_id: str = GiftFields.gift_id
