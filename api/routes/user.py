from fastapi import APIRouter, Depends, HTTPException, status, Response
from . import API_PREFIX, oauth2_scheme
from api.schemas.user import CreateUser, UserQuery, APIUserCreation, UserUpdateSchema
from api.services.user import UserBuilder
from api.db.session import get_db
from uuid import UUID   
from sqlalchemy.orm import Session
from hashlib import sha3_512
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

@router.get("/me")
def read_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    usr = UserBuilder(db)

    usr = usr.get_user(UserQuery(id=UUID(payload.get("sub"))))
    del usr.password
    
    return usr


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "User deleted successfully"},
        401: {"description": "Invalid token"},
        404: {"description": "User not found"},
    }
)
def delete_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        user_id = UUID(payload["sub"])
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format")

    usr = UserBuilder(db)
    lo_usr = usr.get_user(UserQuery(id=user_id))
    if not lo_usr:
        raise HTTPException(status_code=404, detail="User not found")

    usr.delete_user(UserQuery(id=user_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/business-role", status_code=status.HTTP_200_OK, 
            responses={
                200: {"description": "Business role updated successfully"},
                401: {"description": "Invalid token"},
                404: {"description": "User not found"},
                400: {"description": "Invalid business role"},
                
            })
def add_business_role(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db),
    business_role: str = "business"
):
    payload = verify_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        user_id = UUID(payload["sub"])
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format")

    usr = UserBuilder(db)
    lo_usr = usr.get_user(UserQuery(id=user_id))
    if not lo_usr:
        raise HTTPException(status_code=404, detail="User not found")
    
    if business_role not in ["business", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid business role")

    usr.add_business_role(UserQuery(id=user_id), business_role)
    
    return {"message": "Business role updated successfully"}