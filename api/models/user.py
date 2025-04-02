from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from uuid import uuid4
import uuid
from api.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        comment="Unique user ID for users",
    )
    email = Column(
        String(length=255),
        unique=True,
        index=True,
        nullable=False,
        comment="Email address for user",
    )
    date_registered = Column(
        DateTime, nullable=False, default=datetime.now, comment="Date user registered"
    )
    date_updated = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
        comment="Date user updated",
    )
    is_active = Column(Boolean, default=True, comment="User account active status")
    username = Column(
        String(length=64),
        unique=True,
        index=True,
        nullable=False,
        comment="Username for user",
    )
    password = Column(
        String(length=255), nullable=False, comment="Hashed password for user"
    )

