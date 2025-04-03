
# services/roles.py
from sqlalchemy.orm import Session
from api.crud import roles as crud_roles
from api.schemas.roles import BusinessRoleCreate, PermissionCreate, RolePermissionCreate
from api.models.roles import BusinessRole, Permission, RolePermission

# --- BusinessRole Services ---
def create_business_role(db, role_data):
    existing = db.query(BusinessRole).filter(BusinessRole.name == role_data.name).first()
    if existing:
        raise ValueError(f"Business role '{role_data.name}' already exists.")
    return crud_roles.create_business_role(db, role_data)

def delete_business_role(db, role_id):
    if not crud_roles.delete_business_role(db, role_id):
        raise LookupError("Role not found.")

def update_business_role(db, role_id, role_data):
    updated = crud_roles.update_business_role(db, role_id, role_data)
    if not updated:
        raise LookupError("Role not found.")
    return updated

def get_business_role_by_id(db, role_id):
    role = crud_roles.get_business_role(db, role_id)
    if not role:
        raise LookupError("Role not found.")
    return role

def list_business_roles(db):
    return crud_roles.get_all_business_roles(db)


# --- Permission Services ---
def create_permission(db, permission_data):
    existing = db.query(Permission).filter(Permission.name == permission_data.name).first()
    if existing:
        raise ValueError(f"Permission '{permission_data.name}' already exists.")
    return crud_roles.create_permission(db, permission_data)

def delete_permission(db, permission_id):
    if not crud_roles.delete_permission(db, permission_id):
        raise LookupError("Permission not found.")

def update_permission(db, permission_id, permission_data):
    updated = crud_roles.update_permission(db, permission_id, permission_data)
    if not updated:
        raise LookupError("Permission not found.")
    return updated

def get_permission_by_id(db, permission_id):
    perm = crud_roles.get_permission(db, permission_id)
    if not perm:
        raise LookupError("Permission not found.")
    return perm

def list_permissions(db):
    return crud_roles.get_all_permissions(db)


# --- RolePermission Services ---
def assign_permission_to_role(db, data):
    existing = db.query(RolePermission).filter(
        RolePermission.role_id == data.role_id,
        RolePermission.permission_id == data.permission_id
    ).first()
    if existing:
        raise ValueError("This permission is already assigned to the role.")
    return crud_roles.create_role_permission(db, data)

def remove_permission_from_role(db, role_permission_id):
    if not crud_roles.delete_role_permission(db, role_permission_id):
        raise LookupError("Role-permission link not found.")

def list_role_permissions(db):
    return crud_roles.get_all_role_permissions(db)
