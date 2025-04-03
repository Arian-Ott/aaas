# schemas/roles.py
from pydantic import BaseModel

# --- Base Classes ---
class BusinessRoleBase(BaseModel):
    name: str
    description: str

class PermissionBase(BaseModel):
    name: str
    description: str

class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int


# --- Create Schemas ---
class BusinessRoleCreate(BusinessRoleBase):
    pass

class PermissionCreate(PermissionBase):
    pass

class RolePermissionCreate(RolePermissionBase):
    pass


# --- Read/Response Schemas ---
class BusinessRoleRead(BusinessRoleBase):
    id: int
    class Config:
        orm_mode = True

class PermissionRead(PermissionBase):
    id: int
    class Config:
        orm_mode = True

class RolePermissionRead(RolePermissionBase):
    id: int
    class Config:
        orm_mode = True

