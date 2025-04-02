from api.models.roles import BusinessRole, Permission, RolePermission
from sqlalchemy.orm import Session
from api.schemas.roles import CreateRole, RoleQuery, PermissionSchema, PermissionQuery

from typing import List

def create_permission(db: Session, permission: PermissionSchema):
    new_permission = Permission(**permission.model_dump(exclude_unset=True))
    if db.query(Permission).filter(Permission.name == new_permission.name).first():
        return None
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission


def create_role(db: Session, role: CreateRole):
    """
    Creates a new BusinessRole instance using data from the CreateRole schema.
    Commits the new role to the database.
    """
    
    new_role = BusinessRole(**role.model_dump(exclude_none=True, exclude_unset=False))
    
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    return new_role

def get_role(db:Session, role:RoleQuery):
    if role.id:
        return db.query(BusinessRole).filter(BusinessRole.id == role.id).first()
    if role.name:
        return db.query(BusinessRole).filter(BusinessRole.name == role.name).first()
    return None

def get_permission(db:Session, permission:PermissionQuery):
    if permission.id:
        return db.query(Permission).filter(Permission.id == permission.id).first()
    if permission.name:
        return db.query(Permission).filter(Permission.name == permission.name).first()
    return None


def map_role_permission(db:Session, role:RoleQuery, permission: PermissionQuery):
    lv_role = get_role(db, role)
    lv_permission = get_permission(db, permission)
    if lv_role is None:
        raise ValueError("Role not found")
    if lv_permission is None:
        raise ValueError("Permission not found")
    if db.query(RolePermission).filter(RolePermission.role_id == lv_role.id, RolePermission.permission_id == lv_permission.id).first():
        raise ValueError("Role-Permission mapping already exists")

    role_permission = RolePermission(role_id=lv_role.id, permission_id=lv_permission.id)
    db.add(role_permission)
    db.commit()
    db.refresh(role_permission)
    return role_permission

    
        
#TODO: Add tests for the above functions
#TODO: Add functions for CRUD operations on roles and permissions
