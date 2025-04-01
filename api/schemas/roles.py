from pydantic import BaseModel, EmailStr, ConfigDict

from typing import Optional, Union

class PermissionSchema(BaseModel):
    name:str
    description:str
    model_config = ConfigDict(from_attributes=True)

class PermissionQuery(BaseModel):
    name:Optional[str]
    id:Optional[int]
    model_config = ConfigDict(from_attributes=True)

class CreateRole(BaseModel):
    name:str
    description:str

    model_config = ConfigDict(from_attributes=True)
    
class RoleQuery(BaseModel):
    name:Optional[str]
    id:Optional[int]
    model_config = ConfigDict(from_attributes=True)

class BusinessRole(BaseModel):
    name:str
    description:str