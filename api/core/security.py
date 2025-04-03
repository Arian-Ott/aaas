import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from api.core.config import settings
from uuid import UUID   
if not os.path.exists("api/core/certs/ec-private.pem"):
    raise FileNotFoundError("Private key not found")
if not os.path.exists("api/core/certs/ec-public.pem"):
    raise FileNotFoundError("Public key not found")


with open("api/core/certs/ec-private.pem", "r") as f:
    PRIVATE_KEY = f.read()

with open("api/core/certs/ec-public.pem", "r") as f:
    PUBLIC_KEY = f.read()




def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """create_access_token Generates a JWT token with the given data and expiration time.

    :param dict data: JWT payload data
    :param timedelta expires_delta: Expiration time for the token
    :return str: JWT token
    """
    
    to_encode = data.copy()
    
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """verify_token Verifies the given token and returns the payload.

    :param str token: JWT token
    :raises ValueError: If the token is invalid
    :return dict: JWT payload
    """
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {e}")

