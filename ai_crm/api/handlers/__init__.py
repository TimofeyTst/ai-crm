from ai_crm.pkg.models.base import router
from ai_crm.api.handlers import users

__router__ = router.Router(
    routers=(
        users.user_router,
    ),
)
