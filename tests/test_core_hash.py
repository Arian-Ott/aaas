from api.core.hashing import get_password_hash, verify_password
from uuid import uuid4

test_pw = uuid4().hex


def test_verify_password():
    hashed_password = get_password_hash(test_pw)
    assert verify_password(test_pw, hashed_password), (
        "Password should match hashed password"
    )


def test_get_password_hash():
    hashed_password = get_password_hash(test_pw)
    assert hashed_password != test_pw, (
        "Hashed password should not be equal to the password"
    )
    assert len(hashed_password) == 97, "Hashed password should be 97 characters long"
