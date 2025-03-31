import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import app
from api.db.session import get_db, Base
from api.models.user import User
import os

from uuid import uuid4
import random
import string

# ------------------------
# 🔧 SQLite Test DB Setup
# ------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ------------------------
# 🔁 Dependency Override
# ------------------------


def override_get_db():
    try:
        Base.metadata.create_all(bind=engine)
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        os.remove("./test.db")


app.dependency_overrides[get_db] = override_get_db


# ------------------------
# 🧪 Core Fixtures
# ------------------------
@pytest.fixture(scope="function")
def db():
    # Drop and recreate tables around each test

    Base.metadata.create_all(
        bind=engine,
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c


# ------------------------
# 🏭 User Factory
# ------------------------
