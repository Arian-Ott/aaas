import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import app
from api.db.session import get_db
from api.models.user import User
from api.core.security import get_password_hash

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
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ------------------------
# 🧪 Core Fixtures
# ------------------------
@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

# ------------------------
# 🏭 User Factory
# ------------------------
def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

@pytest.fixture
def create_user(db):
    def _create_user(
        email: str = None,
        username: str = None,
        password: str = "testpassword123",
        is_superuser: bool = False,
    ) -> User:
        email = email or f"{random_string()}@example.com"
        username = username or f"user_{random_string()}"
        user = User(
            id=uuid4(),
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_superuser=is_superuser,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        user.raw_password = password  # for test login
        return user
    return _create_user

# ------------------------
# 🔐 Authenticated Clients
# ------------------------
@pytest.fixture
def authenticated_client(client, create_user):
    user = create_user()
    response = client.post("/api/v1/auth/login", data={
        "username": user.email,
        "password": user.raw_password
    })
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

@pytest.fixture
def admin_client(client, create_user):
    admin = create_user(is_superuser=True)
    response = client.post("/api/v1/auth/login", data={
        "username": admin.email,
        "password": admin.raw_password
    })
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client