from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.db.session import get_db
from api.services import roles as role_service
from api.schemas.roles import (
    BusinessRoleCreate, BusinessRoleRead,
    PermissionCreate, PermissionRead,
    RolePermissionCreate, RolePermissionRead
)

router = APIRouter(prefix="/roles", tags=["Roles"])


# --- Business Role Endpoints ---

@router.post("/", response_model=BusinessRoleRead, status_code=status.HTTP_201_CREATED)
def create_role(role: BusinessRoleCreate, db: Session = Depends(get_db)):
    try:
        return role_service.create_business_role(db, role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[BusinessRoleRead])
def list_roles(db: Session = Depends(get_db)):
    return role_service.list_business_roles(db)


@router.get("/{role_id}", response_model=BusinessRoleRead)
def get_role(role_id: int, db: Session = Depends(get_db)):
    try:
        return role_service.get_business_role_by_id(db, role_id)
    except LookupError:
        raise HTTPException(status_code=404, detail="Role not found")


@router.put("/{role_id}", response_model=BusinessRoleRead)
def update_role(role_id: int, role: BusinessRoleCreate, db: Session = Depends(get_db)):
    try:
        return role_service.update_business_role(db, role_id, role)
    except LookupError:
        raise HTTPException(status_code=404, detail="Role not found")


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    try:
        role_service.delete_business_role(db, role_id)
    except LookupError:
        raise HTTPException(status_code=404, detail="Role not found")


# --- Permission Endpoints ---

@router.post("/permissions", response_model=PermissionRead, status_code=status.HTTP_201_CREATED)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    try:
        return role_service.create_permission(db, permission)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/permissions", response_model=list[PermissionRead])
def list_permissions(db: Session = Depends(get_db)):
    return role_service.list_permissions(db)


@router.get("/permissions/{permission_id}", response_model=PermissionRead)
def get_permission(permission_id: int, db: Session = Depends(get_db)):
    try:
        return role_service.get_permission_by_id(db, permission_id)
    except LookupError:
        raise HTTPException(status_code=404, detail="Permission not found")


@router.put("/permissions/{permission_id}", response_model=PermissionRead)
def update_permission(permission_id: int, permission: PermissionCreate, db: Session = Depends(get_db)):
    try:
        return role_service.update_permission(db, permission_id, permission)
    except LookupError:
        raise HTTPException(status_code=404, detail="Permission not found")


@router.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    try:
        role_service.delete_permission(db, permission_id)
    except LookupError:
        raise HTTPException(status_code=404, detail="Permission not found")


# --- RolePermission Endpoints ---

@router.post("/assign", response_model=RolePermissionRead, status_code=status.HTTP_201_CREATED)
def assign_permission(data: RolePermissionCreate, db: Session = Depends(get_db)):
    try:
        return role_service.assign_permission_to_role(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/assignments", response_model=list[RolePermissionRead])
def list_role_permissions(db: Session = Depends(get_db)):
    return role_service.list_role_permissions(db)


@router.delete("/assign/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_permission(assignment_id: int, db: Session = Depends(get_db)):
    try:
        role_service.remove_permission_from_role(db, assignment_id)
    except LookupError:
        raise HTTPException(status_code=404, detail="Assignment not found")
