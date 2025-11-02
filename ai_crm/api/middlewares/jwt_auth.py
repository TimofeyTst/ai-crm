"""JWT authentication dependency for protecting routes."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ai_crm.internal.services import auth as auth_service
from ai_crm.pkg.context import web_context
from ai_crm.pkg.models.ai_crm import user as user_models
from ai_crm.pkg.models.exceptions import auth as auth_exceptions, users as users_exceptions

# HTTPBearer security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    web_context: web_context.WebContext = Depends(web_context.get_web_context_dependency())
) -> user_models.User:
    """Dependency to get current authenticated user from JWT token.

    Args:
        credentials: HTTPBearer credentials containing JWT token.
        web_context: Application web context.

    Returns:
        Current authenticated user.

    Raises:
        HTTPException: If token is invalid or user is not found.
    """
    token = credentials.credentials
    
    try:
        user = await auth_service.get_current_user(web_context, token)
        return user
    except auth_exceptions.InvalidToken:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (users_exceptions.InactiveUser, users_exceptions.UserNotFound):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive or not found",
        )
