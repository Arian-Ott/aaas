from fastapi import APIRouter
from . import API_PREFIX
router = APIRouter(prefix=API_PREFIX + "users", tags=["users"])

@router.options("")
async def options_users():
    return {"methods": ["GET", "POST"]}

