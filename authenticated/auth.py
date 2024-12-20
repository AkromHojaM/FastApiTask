import os

from dns.dnssecalgs import algorithms
from dotenv import load_dotenv
from sqlalchemy import select,insert
from passlib.context import CryptContext
from sqlalchemy.util import deprecated

from data.databse import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User
from fastapi import APIRouter,Depends,HTTPException
from .schemes import RegisterUser, UserInDb, UserLogin
from .utils import generate_token

load_dotenv()
user = APIRouter()
algorithm = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

@user.post("/register_user/")
async def register_user(model:RegisterUser,
                        session:AsyncSession = Depends(get_async_session)):
    if model.password1 != model.password2:
        raise HTTPException(status_code=400,detail="The wrong password")
    username_exists = (await session.execute(select(User).where(User.username == model.username))).scalar_one_or_none()
    email_exists = (await session.execute(select(User).where(User.email == model.email))).scalar_one_or_none()

    if username_exists:
        raise HTTPException(status_code=400,detail="Username Already In Use")

    if email_exists:
        raise HTTPException(status_code=400,detail="Emai; Alreadt In Use")

    hashed_password = pwd_context.hash(model.password2)
    await session.execute(insert(User).values(firstname = model.firstname,
                                              lastname = model.lastname,
                                              username = model.username,
                                              email = model.email,
                                              password = hashed_password))
    await session.commit()
    return {"success":True,"username":model.username,"email":model.email,
            "Data":"User Registred Successfully"}



@user.post("/login/")
async def login(model:UserLogin,
                session:AsyncSession = Depends(get_async_session)):
    user_data = await session.execute(select(User).where(User.username == model.username))
    result = user_data.scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=401 , detail="Invalid Username or Password!")

    if not pwd_context.verify(model.password , result.password):
        raise HTTPException(status_code=401, detail="Invalid Username or Password!")

    token = generate_token(result.id)
    return {"token":token,"username":result.username}