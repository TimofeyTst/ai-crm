from ai_crm.api.handlers import auth, gifts, users
from ai_crm.pkg.models.base import router

__router__ = router.Router(
    routers=(
        auth.auth_router,
        users.user_router,
        gifts.gift_router,
    ),
)
