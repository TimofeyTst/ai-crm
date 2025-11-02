from ai_crm.pkg.models.base import router
from ai_crm.api.handlers import users, gifts, auth

__router__ = router.Router(
    routers=(
        auth.auth_router,
        users.user_router,
        gifts.gift_router,
    ),
)
