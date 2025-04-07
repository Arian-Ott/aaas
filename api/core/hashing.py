from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], default="argon2", deprecated="auto",argon2__memory_cost=131072,   # 128 MiB – better than OWASP baseline
    argon2__time_cost=5,          # 5 iterations – above most current recommendations
    argon2__parallelism=2 )


def get_password_hash(password: str):
    """get_password_hash returns an argon2id hashed password

    :param str password: Plain text password
    :return str: Hashed password 
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """verify_password Verifies a plain text password against a hashed password

    :param str plain_password: Plain text password
    :param str hashed_password: Hashed password
    :return bool: True if the passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)
