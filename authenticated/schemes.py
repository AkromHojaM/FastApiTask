from datetime import datetime
from pydantic import BaseModel





class RegisterUser(BaseModel):
    firstname:str
    lastname:str
    username:str
    email:str
    password1:str
    password2:str



class UserInDb(BaseModel):
    firstname:str
    lastname:str
    username:str
    email:str
    password:str
