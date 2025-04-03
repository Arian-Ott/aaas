from uuid import uuid4
import pytest
from sqlalchemy.orm import Session

from api.services.user import UserBuilder
from api.schemas.user import UserQuery
from api.crud.user import get_user
from api.db.session import Base, engine, SessionLocal


class TestUserBuilder:
    def setup_method(self):
        # Ensure a clean database before each test
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.db: Session = SessionLocal()

    def teardown_method(self):
        # Clean up the database after each test
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    def test_create_user_success(self):
        builder = UserBuilder(self.db)
        builder.set_username("builderuser1")
        builder.set_password("strongpass123")
        builder.set_email("builder1@example.com")
        user = builder.commit()
        self.db.refresh(user)
        assert user.username == "builderuser1"
        assert user.email == "builder1@example.com"
        assert user.is_active

    def test_direct_create_user(self):
        from api.schemas.user import CreateUser
        from api.crud.user import create_user

        user = create_user(
            self.db,
            CreateUser(
                id=uuid4(),
                username="sanityuser",
                password="plaintext",  # just for test
                email="sanity@example.com",
                is_active=True,
            ),
        )
        assert user.username == "sanityuser"

    def test_duplicate_email_raises(self):
        builder1 = UserBuilder(self.db)
        builder1.set_username("builderuser2")
        builder1.set_password("securepass456")
        builder1.set_email("dupe@example.com")
        builder1.commit()

        builder2 = UserBuilder(self.db)
        builder2.set_username("otheruser")
        builder2.set_password("securepass456")

        with pytest.raises(ValueError, match="Email already exists"):
            builder2.set_email("dupe@example.com")

    def test_duplicate_username_raises(self):
        builder1 = UserBuilder(self.db)
        builder1.set_username("dupeuser")
        builder1.set_password("securepass456")
        builder1.set_email("first@example.com")
        builder1.commit()

        builder2 = UserBuilder(self.db)
        builder2.set_password("securepass456")
        builder2.set_email("second@example.com")

        with pytest.raises(ValueError, match="Username already exists"):
            builder2.set_username("dupeuser")

    def test_short_password_raises(self):
        builder = UserBuilder(self.db)
        with pytest.raises(ValueError, match="Password too short"):
            builder.set_password("short")

    def test_invalid_username_raises(self):
        builder = UserBuilder(self.db)
        with pytest.raises(ValueError, match="Invalid username"):
            builder.set_username("a")

    def test_missing_fields_on_commit(self):
        builder = UserBuilder(self.db)
        builder.set_username("missingfields")
        builder.set_password("securepass123")
        with pytest.raises(ValueError, match="Missing required fields"):
            builder.commit()

    def test_create_then_query(self):
        email = "querytest@example.com"
        builder = UserBuilder(self.db)
        builder.set_username("querytestuser")
        builder.set_password("complexpass123")
        builder.set_email(email)
        user = builder.commit()

        queried = get_user(self.db, UserQuery(email=email))
        assert queried is not None
        assert queried.username == "querytestuser"

    def test_delete_user(self):
        email = uuid4().hex + "@example.com"
        builder = UserBuilder(self.db)
        builder.set_username("deleteuser")
        builder.set_password("complexpass123")
        builder.set_email(email)
        user = builder.commit()
        assert user is not None
        builder.delete_user(UserQuery(email=email))
        queried = get_user(self.db, UserQuery(email=email))
        assert queried is None, "User should be deleted"
        