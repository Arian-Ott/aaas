from fastapi import APIRouter, Depends, HTTPException
from . import API_PREFIX
from api.schemas.user import CreateUser, UserQuery
from api.services.user import UserBuilder
from api.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix=API_PREFIX + "/users", tags=["users"])


@router.post("/register")
async def register(usr: CreateUser, db: Session = Depends(get_db)):
    user = UserBuilder(db)
    if user.get_user(
        UserQuery(username=usr.username) if usr.username else UserQuery(email=usr.email)
    ):
        raise HTTPException(status_code=400, detail="User already exists")
    user.set_username(usr.username)
    user.set_password(usr.password)
    user.set_email(usr.email)
    user.commit()
    return {"message": "User created successfully"}
