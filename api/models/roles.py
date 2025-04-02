from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from api.db.session import Base

class BusinessRole(Base):
    __tablename__ = "business_roles"
    id = Column(Integer, primary_key=True, index=True, comment="Role ID", autoincrement=True)
    name = Column(String(length=64), unique=True, index=True, nullable=False, comment="Role name")
    description = Column(String(length=255), nullable=False, comment="Role description")
    

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True, comment="Permission ID", autoincrement=True)
    name = Column(String(length=64), unique=True, index=True, nullable=False, comment="Permission name")
    description = Column(String(length=255), nullable=False, comment="Permission description")
    

class RolePermission(Base):
    __tablename__ = "role_permissions"
    id = Column(Integer, primary_key=True, index=True, comment="Role Permission ID", autoincrement=True)
    role_id = Column(Integer, ForeignKey('business_roles.id'), nullable=False, comment="Role ID")
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False, comment="Permission ID")
    
    role = relationship("BusinessRole", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")