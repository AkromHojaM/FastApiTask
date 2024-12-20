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


class ProductSale(BaseModel):
    product_id:int
    discount:int
    limit:int


class ProductAddCategory(BaseModel):
    product_id:int
    category_id:int
