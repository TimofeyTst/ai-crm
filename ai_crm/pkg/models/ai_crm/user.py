from pydantic import EmailStr
from datetime import datetime
import typing as tp

from pydantic.fields import Field

from ai_crm.pkg.models.base import model as base_models

class UserFields:
    id: str = Field(description="User id.", example="uuid")
    username: str = Field(description="User name.", example="Moscow")
    email: EmailStr = Field(description="User email.", example="MSK")
    password_hash: str = Field(description="User password hash.", example=1)
    first_name: str | None = Field(description="User first name.", example="Moscow")
    last_name: str | None = Field(description="User last name.", example="Moscow")
    is_active: bool = Field(description="User is active.", example=True)
    created_at: datetime = Field(description="User created at.", example=datetime.now())
    updated_at: datetime = Field(description="User updated at.", example=datetime.now())

# Models
class User(base_models.BaseModel):
    id: str = UserFields.id
    username: str = UserFields.username
    email: EmailStr = UserFields.email
    password_hash: str = UserFields.password_hash
    first_name: str | None = UserFields.first_name
    last_name: str | None = UserFields.last_name
    is_active: bool = UserFields.is_active
    created_at: datetime = UserFields.created_at
    updated_at: datetime = UserFields.updated_at

# Requests
class UserCreateRequest(base_models.BaseModel):
    username: str = UserFields.username
    email: EmailStr = UserFields.email
    password_hash: str = UserFields.password_hash
    first_name: str | None = UserFields.first_name
    last_name: str | None = UserFields.last_name
    is_active: bool = UserFields.is_active
