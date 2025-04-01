import pytest
from uuid import uuid4
from api.schemas.user import CreateUser, UserQuery
from api.crud.user import *
import sqlalchemy
from api.db.session import Base, engine, SessionLocal
import uuid


class TestUserCrud:
    def setup_method(self):
        # Reset the database (drop and recreate tables)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

        # Create a user with a unique ID/email
        self.test_user = CreateUser(
            id=uuid4(),
            username=f"testuser_{uuid4().hex}",
            password="strongpassword123",
            email=f"test_{uuid4()}@example.com",
            is_active=True,
        )

    def teardown_method(self):
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    def test_create_user(self):
        user = create_user(self.db, self.test_user)

        print(type(user.id), type(self.test_user.id))
        assert user.id == self.test_user.id, (
            f"Expected {self.test_user.id}, but got {user.id}"
        )
        assert user.username == self.test_user.username, (
            f"Expected {self.test_user.username}, but got {user.username}"
        )
        assert user.email == self.test_user.email, (
            f"Expected {self.test_user.email}, but got {user.email}"
        )
        assert user.is_active == self.test_user.is_active, (
            f"Expected {self.test_user.is_active}, but got {user.is_active}"
        )

    def test_get_user(self):
        user = create_user(self.db, self.test_user)

        user_query = UserQuery(id=user.id)
        print(user_query)
        user = get_user(self.db, user_query)
        assert user.id == self.test_user.id, (
            f"Expected {self.test_user.id}, but got {user.id}"
        )
        assert user.username == self.test_user.username, (
            f"Expected {self.test_user.username}, but got {user.username}"
        )
        assert user.email == self.test_user.email, (
            f"Expected {self.test_user.email}, but got {user.email}"
        )
        assert user.is_active == self.test_user.is_active, (
            f"Expected {self.test_user.is_active}, but got {user.is_active}"
        )

    def test_get_user_no_user(self):
        user_query = UserQuery(id=uuid4())

        with pytest.raises(ValueError):
            get_user(self.db, user_query)

    def test_create_multiple_users(self):
        create_user(self.db, self.test_user)
        with pytest.raises(sqlalchemy.exc.IntegrityError):
            create_user(self.db, self.test_user)

    def test_get_all_users(self):
        lt_users = []
        for _ in range(5):
            ls_user = CreateUser(
                id=uuid4(),
                username=f"testuser_{uuid4().hex}",
                password="strongpassword123",
                email=f"test_{uuid4()}@example.com",
                is_active=True,
            )
            lt_users.append(ls_user)
            create_user(self.db, ls_user)

        users = get_users(self.db)
        assert len(users) == 5, f"Expected 5, but got {len(users)}"

    def test_delete_user(self):
        user = create_user(self.db, self.test_user)
        user_query = UserQuery(id=user.id)
        get_user(self.db, user_query)
        delete_user(self.db, user_query)
        with pytest.raises(ValueError):
            get_user(self.db, user_query)

    def test_update_user(self):
        user = create_user(self.db, self.test_user)
        user_query = UserQuery(id=user.id)
        updated_user = CreateUser(
            id=user.id,
            username=f"updated_{user.username}",
            password=f"updated_{user.password}",
            email=f"updated_{user.email}",
            is_active=not user.is_active,
        )
        update_user(self.db, user_query, updated_user)
        user = get_user(self.db, user_query)
        assert user.id == updated_user.id, (
            f"Expected {updated_user.id}, but got {user.id}"
        )
        assert user.username == updated_user.username, (
            f"Expected {updated_user.username}, but got {user.username}"
        )
        assert user.email == updated_user.email, (
            f"Expected {updated_user.email}, but got {user.email}"
        )

        assert user.is_active == updated_user.is_active, (
            f"Expected {updated_user.is_active}, but got {user.is_active}"
        )
