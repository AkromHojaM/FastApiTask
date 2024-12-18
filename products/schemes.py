from datetime import datetime
from pydantic import BaseModel




class Product(BaseModel):
    name:str
    description:str
    price:float
    count:int

class ProductUpdate(BaseModel):
    name:str
    description:str
    price:float
    count:int


