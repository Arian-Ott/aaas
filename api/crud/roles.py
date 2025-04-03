
# crud/roles.py
from sqlalchemy.orm import Session
from api.models.roles import BusinessRole, Permission, RolePermission
from api.schemas.roles import BusinessRoleCreate, PermissionCreate, RolePermissionCreate

# --- BusinessRole CRUD ---
def get_business_role(db, role_id):
    return db.query(BusinessRole).filter(BusinessRole.id == role_id).first()

def get_all_business_roles(db):
    return db.query(BusinessRole).all()

def create_business_role(db, role_data):
    db_role = BusinessRole(**role_data.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_business_role(db, role_id, role_data):
    db_role = get_business_role(db, role_id)
    if not db_role:
        return None
    for key, value in role_data.dict().items():
        setattr(db_role, key, value)
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_business_role(db, role_id):
    db_role = get_business_role(db, role_id)
    if not db_role:
        return False
    db.delete(db_role)
    db.commit()
    return True


# --- Permission CRUD ---
def get_permission(db, permission_id):
    return db.query(Permission).filter(Permission.id == permission_id).first()

def get_all_permissions(db):
    return db.query(Permission).all()

def create_permission(db, permission_data):
    db_perm = Permission(**permission_data.dict())
    db.add(db_perm)
    db.commit()
    db.refresh(db_perm)
    return db_perm

def update_permission(db, permission_id, permission_data):
    db_perm = get_permission(db, permission_id)
    if not db_perm:
        return None
    for key, value in permission_data.dict().items():
        setattr(db_perm, key, value)
    db.commit()
    db.refresh(db_perm)
    return db_perm

def delete_permission(db, permission_id):
    db_perm = get_permission(db, permission_id)
    if not db_perm:
        return False
    db.delete(db_perm)
    db.commit()
    return True


# --- RolePermission CRUD ---
def get_role_permission(db, role_permission_id):
    return db.query(RolePermission).filter(RolePermission.id == role_permission_id).first()

def get_all_role_permissions(db):
    return db.query(RolePermission).all()

def create_role_permission(db, rp_data):
    db_rp = RolePermission(**rp_data.dict())
    db.add(db_rp)
    db.commit()
    db.refresh(db_rp)
    return db_rp

def delete_role_permission(db, role_permission_id):
    db_rp = get_role_permission(db, role_permission_id)
    if not db_rp:
        return False
    db.delete(db_rp)
    db.commit()
    return True