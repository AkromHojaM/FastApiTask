import os
import jwt
import secrets
from dotenv import load_dotenv
from datetime import datetime,timedelta
from fastapi import Depends,HTTPException
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from passlib.context import CryptContext
from passlib.handlers.bcrypt import bcrypt
from typing_extensions import deprecated



load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in environment variables")




security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")


def generate_token(user_id:int):
    jti_access = secrets.token_urlsafe(32)
    jti_refresh = secrets.token_urlsafe(32)

    payload_access = {
        'type':'access',
        'exp':datetime.utcnow() + timedelta(minutes=30),
        'user_id':user_id,
        'jti':jti_access
    }


    payload_refresh = {
        'type':'refresh',
        'exp':datetime.utcnow() + timedelta(days=1),
        'user_id':user_id,
        'jti':jti_refresh
    }

    access_token = jwt.encode(payload_access,SECRET_KEY,algorithm="HS256")
    refresh_token = jwt.encode(payload_refresh,SECRET_KEY,algorithm="HS256")

    return {
        'access':access_token,
        'refresh':refresh_token
    }

def verify_token(credentials:HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid Token")
