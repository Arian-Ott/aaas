from . import API_PREFIX
from uuid import uuid4
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.core.hashing import verify_password
from api.core.security import create_access_token, verify_token

from api.db.session import get_db
from api.services.user import UserBuilder
from api.schemas.user import UserLogin, UserQuery

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=API_PREFIX + "/sagw/token")
sapi_router = APIRouter(prefix=API_PREFIX + "/sagw", tags=["sagw"])


@sapi_router.get("/public_key")
async def public_key():
    """Return the public key for the API."""
    with open("api/core/certs/ec-public.pem", "r") as f:
        return {"public_key": f.read(), "alg": "ES512", "use": "sig"}


@sapi_router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    usr = UserBuilder(db)
    if not usr.get_user(UserQuery(username=user.username, email=user.email)):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = usr.get_user(UserQuery(username=user.username, email=user.email)).id
    token_id = uuid4().hex
    access_token = create_access_token(
        data={
            "sub": str(user_id),
            "jti": token_id,
            "scope": "me",
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}


@sapi_router.post("/token")
async def login_with_form(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    usr = UserBuilder(db)
    user = usr.get_user(UserQuery(username=form_data.username))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_id = uuid4().hex
    access_token = create_access_token(
        data={"sub": str(user.id), "jti": token_id, "scope": "me"}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@sapi_router.get("/me")
def read_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    usr = UserBuilder(db)

    usr = usr.get_user(UserQuery(id=UUID(payload.get("sub"))))
    del usr.password
    return usr
