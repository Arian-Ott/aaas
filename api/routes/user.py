from fastapi import APIRouter, Depends, HTTPException
from . import API_PREFIX, oauth2_scheme
from api.schemas.user import CreateUser, UserQuery, APIUserCreation, UserUpdateSchema
from api.services.user import UserBuilder
from api.db.session import get_db
from uuid import UUID   
from sqlalchemy.orm import Session
from api.core.security import create_access_token, verify_token
router = APIRouter(prefix=API_PREFIX + "/users", tags=["users"])


@router.post("/register")
async def register(usr: APIUserCreation, db: Session = Depends(get_db)):
    user = UserBuilder(db)
    if user.get_user(
        UserQuery(username=usr.username) if usr.username else UserQuery(email=usr.email)
    ):
        raise HTTPException(status_code=400, detail="User already exists")
    
    if user.get_user(UserQuery(email=usr.email)):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user.set_username(usr.username)
    user.set_password(usr.password)
    user.set_email(usr.email)
    user = user.commit()
    
    user = {"id": user.id, "username": user.username, "email": user.email, "is_active": user.is_active}
    return user
@router.post("/update")
def update_user(usr: UserUpdateSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    token = dict(verify_token(token))
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = UserBuilder(db)
    lo_user = user.get_user(UserQuery(id=UUID(token.get("sub"))))
    if not lo_user: 
        raise HTTPException(status_code=404, detail="User not found")
    
    
    user.set_username(usr.username)
  
    user.set_email(usr.email)
    user = user.update_user(UserQuery(id=UUID(token.get("sub"))), usr)
    
    return user

@router.get("/all")
def get_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    token = dict(verify_token(token))
    print(token)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = UserBuilder(db)
    lo_user = user.get_user(UserQuery(id=UUID(token.get("sub"))))
    if not lo_user:
        raise HTTPException(status_code=404, detail="User not found")
    users = user.get_users()
    return users