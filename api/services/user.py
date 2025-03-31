from uuid import uuid4
from api.schemas.user import CreateUser, UserQuery
from api.crud.user import get_user, update_user, create_user
from api.core.hashing import get_password_hash
from sqlalchemy.orm import Session

class UserBuilder:
    def __init__(self, db: Session):
        self._id = uuid4()
        self._username = None
        self._password = None
        self._email = None
        self.db = db

    def set_username(self, username: str):
        if not isinstance(username, str) or not (4 <= len(username) <= 64):
            raise ValueError("Invalid username length")
        try:
            # Check if a user with this username already exists
            existing = get_user(self.db, UserQuery(username=username))
        except ValueError as e:
            # If no user is found, that's our desired result
            if str(e) == "No user found":
                existing = None
            else:
                raise
        if existing:
            raise ValueError("Username already exists")
        self._username = username

    def set_password(self, raw_password: str):
        if not isinstance(raw_password, str) or len(raw_password) < 8:
            raise ValueError("Password too short")
        self._password = get_password_hash(raw_password)

    def set_email(self, email: str):
        try:
            # Check if a user with this email already exists
            existing = get_user(self.db, UserQuery(email=email))
        except ValueError as e:
            if str(e) == "No user found":
                existing = None
            else:
                raise
        if existing:
            raise ValueError("Email already exists")
        self._email = email

    def commit(self):
        if not self._username or not self._password or not self._email:
            raise ValueError("Missing required fields")

        user_data = CreateUser(
            id=self._id,
            username=self._username,
            password=self._password,
            email=self._email,
            is_active=True,
        )
        # Try creating the user; let errors propagate if they occur
        user = create_user(self.db, user_data)
        if user is None:
            raise ValueError("No user found")
        return user