from sqlalchemy.orm import Session
from api.models.roles import  BusinessRole 
from api.schemas.roles import CreateRole

def create_business_roles(db: Session, business_role: CreateRole) -> BusinessRole:
    db_business_role = BusinessRole(
        name=business_role.name,
    )
    db.add(db_business_role)
    db.commit()
    db.refresh(db_business_role)
    return db_business_role
