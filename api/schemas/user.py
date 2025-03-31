from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Union
from uuid import UUID


# ----------------------------
# Shared base for user logic
# ----------------------------
class UserBase(BaseModel):
    email: EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)


# ----------------------------
# Create User Schema
# ----------------------------
class CreateUser(UserBase):
    id: Optional[UUID] = None
    password: str
    is_active: bool = True


# ----------------------------
# User Query for filtering
# ----------------------------
class UserQuery(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    id: Optional[Union[str, UUID]] = None

    model_config = ConfigDict(from_attributes=True)
