import os
from sqlalchemy import  select,insert,update,delete
from fastapi import APIRouter,Depends,HTTPException
from dotenv import load_dotenv
from models.models import Products,Category,ProductCategory,User
from data.databse import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .schemes import Product,ProductUpdate

load_dotenv()
product = APIRouter()

@product.post("/category_added/")
async def category_added(category:str,
                         session:AsyncSession = Depends(get_async_session)):
    if User.is_admin == True:
        query = select(Category).where(Category.category == category)
        res = await session.execute(query)
        result = res.scalar_one_or_none()
        if result:
            return  {"Success":False , "Data":None, "Error":"There is this category!"}
        else:
            query2 = insert(Category).values(category = category)
            await session.execute(query2)
            await session.commit()
            return  {"Success":True , "Data":"Category Added", "Error":None}
    else:return  {"Success":False , "Data":None, "Error":"Sorry Your Not Admin"}


@product.post("/product_added/")
async def product_added(model:Product,
                        session:AsyncSession = Depends(get_async_session)):
    try:
        query = insert(Products).values(name = model.name,
                                        description = model.description,
                                        price = model.price,
                                        count = model.count)
        await session.execute(query)
        await session.commit()
        return  {"Success":True , "Data":"Product Added Success", "Error":None}
    except Exception as e:
        return {"Success":False , "Data":None, "Error":e}



@product.delete("/product_remove/")
async def product_remove(product_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    try:

        query1 = select(Products).where(Products.id == product_id)
        res = await session.execute(query1)
        result = res.scalar_one_or_none()

        if result:

            query2 = delete(Products).where(Products.id == product_id)
            await session.execute(query2)
            await session.commit()
            return {"Success": True, "Data": "Product Successfully Deleted", "Error": None}

        else:
            return {"Success": False, "Data": None, "Error": "Product Not Found"}
    except Exception as e:
        return {"Success": False, "Data": None, "Error": str(e)}