from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db.session import Base

class Role(Base):
    __tablename__ = "roles"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(50), unique=True, nullable=False)
    description: str = Column(String(255), nullable=True)

    # Relationships
    user_roles = relationship("UserRoles", back_populates="role", cascade="all, delete-orphan")
    users = relationship("User", secondary="user_roles", back_populates="roles")

    def __repr__(self):
        return f"<Role(name='{self.name}')>"