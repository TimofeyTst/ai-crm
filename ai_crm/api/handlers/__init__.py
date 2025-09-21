from ai_crm.pkg.models.base import router
from ai_crm.api.handlers import users, gifts

__router__ = router.Router(
    routers=(
        users.user_router,
        gifts.gift_router,
    ),
)
