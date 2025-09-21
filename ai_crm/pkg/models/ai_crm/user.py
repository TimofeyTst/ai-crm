from datetime import datetime
import typing as tp

from pydantic.fields import Field

from ai_crm.pkg.models.base import model as base_models

class UserFields:
    id: int = Field(description="User id.", example=1)
    username: str = Field(description="User name.", example="Moscow")
    email: str = Field(description="User email.", example="MSK")
    password_hash: str = Field(description="User password hash.", example=1)
    first_name: str = Field(description="User first name.", example="Moscow")
    last_name: str = Field(description="User last name.", example="Moscow")
    is_active: bool = Field(description="User is active.", example=True)
    created_at: datetime = Field(description="User created at.", example=datetime.now())
    updated_at: datetime = Field(description="User updated at.", example=datetime.now())

class User(base_models.BaseModel):
    id: int = UserFields.id
    username: str = UserFields.username
    email: str = UserFields.email
    password_hash: str = UserFields.password_hash
    first_name: str = UserFields.first_name
    last_name: str = UserFields.last_name
    is_active: bool = UserFields.is_active
    created_at: datetime = UserFields.created_at
    updated_at: datetime = UserFields.updated_at

class UserCreateRequest(base_models.BaseModel):
    username: str = UserFields.username
    email: str = UserFields.email
    password_hash: str = UserFields.password_hash
    first_name: tp.Optional[str] = Field(None, description="User first name.", example="John")
    last_name: tp.Optional[str] = Field(None, description="User last name.", example="Doe")
    is_active: bool = Field(True, description="User is active.", example=True)
