from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.db.session import Base

class UserRoles(Base):
    __tablename__ = "user_roles"

    user_id: int = Column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: int = Column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")

    def __repr__(self):
        return f"<UserRoles(user_id={self.user_id}, role_id={self.role_id})>"