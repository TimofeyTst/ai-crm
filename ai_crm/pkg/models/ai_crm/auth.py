from pydantic import EmailStr, Field

from ai_crm.pkg.models.base import model as base_models


# Requests
class RegisterRequest(base_models.BaseModel):
    username: str = Field(
        description="Username", max_length=50, example="johndoe"
    )
    email: EmailStr = Field(
        description="User email address", example="user@example.com"
    )
    password: str = Field(
        description="User password", min_length=3, example="password123"
    )
    first_name: str | None = Field(
        None, description="User first name", example="John"
    )
    last_name: str | None = Field(
        None, description="User last name", example="Doe"
    )


class LoginRequest(base_models.BaseModel):
    email: EmailStr = Field(
        description="User email address", example="user@example.com"
    )
    password: str = Field(
        description="User password", min_length=3, example="password123"
    )


class RefreshTokenRequest(base_models.BaseModel):
    refresh_token: str = Field(description="JWT refresh token")


# Responses
class TokenResponse(base_models.BaseModel):
    access_token: str = Field(description="JWT access token")
    refresh_token: str = Field(description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(default=86400, description="seconds")
