from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from api.core.config import settings

if not os.path.exists("api/core/certs/ec-private.pem"):
    raise FileNotFoundError("Private key not found")
if not os.path.exists("api/core/certs/ec-public.pem"):
    raise FileNotFoundError("Public key not found")
 
with open("api/core/certs/ec-private.pem", "r") as f:
    PRIVATE_KEY = f.read()

with open("api/core/certs/ec-public.pem", "r") as f:
    PUBLIC_KEY = f.read()




def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {e}")
