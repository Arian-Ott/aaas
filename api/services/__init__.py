from sqlalchemy.orm import Session
from api.models import BusinessRole

def create_business_roles(db: Session, business_role: CreateBusinessRole) -> BusinessRole:
    db_business_role = BusinessRole(
        rolename=business_role.rolename,
    )
    db.add(db_business_role)
    db.commit()
    db.refresh(db_business_role)
    return db_business_role