from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Union
from uuid import UUID
from pydantic import model_validator


# ----------------------------
# Shared base for user logic
# ----------------------------
class UserBase(BaseModel):
    email: EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(UserBase):
    username: Optional[str]
    email: Optional[EmailStr]
    password: str

    model_config = ConfigDict(from_attributes=True)


# ----------------------------
# Create User Schema
# ----------------------------

class APIUserCreation(BaseModel):
    email: EmailStr = "someone@example.com"
    username: str ="arian.ott"
    password: str ="test1234"

    model_config = ConfigDict(from_attributes=True)

class CreateUser(BaseModel):
    id: Optional[UUID] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str
    is_active: bool = True

    @model_validator(mode="after")
    def validate_either_username_or_email(self):
        if not self.username and not self.email:
            raise ValueError("At least one of username or email must be provided")
        return self


# ----------------------------
# User Query for filtering
# ----------------------------
class UserQuery(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    id: Optional[Union[str, UUID]] = None

    model_config = ConfigDict(from_attributes=True)

class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)