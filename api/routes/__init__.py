from api.core.config import settings
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
API_PREFIX = settings.API_PREFIX
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=API_PREFIX + "/sagw/token")