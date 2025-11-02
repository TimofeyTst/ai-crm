"""JWT token utilities."""

import datetime as dt
from typing import Optional

from jose import JWTError, jwt

from ai_crm.pkg.configuration import settings


def create_access_token(data: dict, expires_delta: Optional[dt.timedelta] = None) -> str:
    """Create JWT access token.

    Args:
        data: Dictionary with data to encode in token (usually contains user_id, username, etc.)
        expires_delta: Optional expiration time. If not provided, uses default from settings.

    Returns:
        Encoded JWT token as string.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = dt.datetime.now(dt.UTC) + expires_delta
    else:
        expire = dt.datetime.now(dt.UTC) + dt.timedelta(
            seconds=settings.ai_crm_env.API.REFRESH_TOKEN_EXPIRE_SECONDS
        )
    
    to_encode.update({
        "exp": expire,
        "iat": dt.datetime.now(dt.UTC), # Issued at
        "type": "access",
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.ai_crm_env.API.JWT_SECRET_KEY.get_secret_value(),
        algorithm=settings.ai_crm_env.API.JWT_ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token.

    Args:
        data: Dictionary with data to encode in token.

    Returns:
        Encoded JWT refresh token as string.
    """
    to_encode = data.copy()
    expire = dt.datetime.now(dt.UTC) + dt.timedelta(
        seconds=settings.ai_crm_env.API.REFRESH_TOKEN_EXPIRE_SECONDS
    )
    
    to_encode.update({
        "exp": expire,
        "iat": dt.datetime.now(dt.UTC), # Issued at
        "type": "refresh",
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.ai_crm_env.API.JWT_SECRET_KEY.get_secret_value(),
        algorithm=settings.ai_crm_env.API.JWT_ALGORITHM
    )
    
    return encoded_jwt


def decode_token(token: str, token_type: str = "access") -> Optional[dict]:
    """Decode and validate JWT token.

    Args:
        token: JWT token string to decode.
        token_type: Expected token type ("access" or "refresh").

    Returns:
        Decoded token payload as dictionary, or None if token is invalid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.ai_crm_env.API.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[settings.ai_crm_env.API.JWT_ALGORITHM]
        )
        
        # Verify token type
        if payload.get("type") != token_type:
            return None
        
        return payload
    except JWTError:
        return None

