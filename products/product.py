import os
from sqlalchemy import  select,insert,update,delete
from fastapi import APIRouter,Depends,HTTPException
from dotenv import load_dotenv

from authenticated.utils import verify_token
from models.models import Products, Category, ProductCategory, User, SaleProducts
from data.databse import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from .schemes import Product, ProductUpdate, ProductSale, ProductAddCategory

load_dotenv()
product = APIRouter()

@product.post("/category_added/")
async def category_added(category:str,
                         token: dict = Depends(verify_token),
                         session:AsyncSession = Depends(get_async_session)):
    user_id = token.get("user_id")
    query = select(User).where(User.id ==  user_id)
    res_user = await session.execute(query)
    rest_user = res_user.scalar()

    if rest_user:
        if rest_user.role_id != 3 != rest_user.role_id != 2:
            return  {"Success":False , "Data":None, "Error":"You are Not Admin!"}
        query2 = select(Category).where(Category.category == category)
        res = await session.execute(query2)
        result = res.scalar_one_or_none()
        if result:
            return  {"Success":False , "Data":None, "Error":"There is this category!"}
        else:
            query3 = insert(Category).values(category = category)
            await session.execute(query3)
            await session.commit()
            return  {"Success":True , "Data":"Category Added", "Error":None}
    else:return  {"Success":False , "Data":None, "Error":"No Data"}


@product.post("/product_added/")
async def product_added(model:Product,
                        token:dict = Depends(verify_token),
                        session:AsyncSession = Depends(get_async_session)):

    try:
        user_id = token.get("user_id")
        query = select(User).where(User.id == user_id)
        res_user = await session.execute(query)
        rest_user = res_user.scalar()
        if rest_user:
            if rest_user.role_id != 3 != rest_user.role_id != 2:
                return  {"Success":False , "Data":None, "Error":"You are Not Admin Or Not Super User"}
            query = insert(Products).values(name = model.name,
                                        description = model.description,
                                        price = model.price,
                                        count = model.count)
            await session.execute(query)
            await session.commit()
            return  {"Success":True , "Data":"Product Added Success", "Error":None}
        else:return  {"Success":False , "Data":None, "Error":"No Data"}
    except Exception as e:
        return {"Success":False , "Data":None, "Error":e}


@product.post("/product_add_sale/")
async def product_add_sale(model:ProductSale,
                           token:dict = Depends(verify_token),
                           session:AsyncSession = Depends(get_async_session)):

    try:
        user_id = token.get("user_id")
        query = select(User).where(User.id == user_id)
        res = await session.execute(query)
        result = res.scalar()
        if result:
            if result.role_id != 3 != result.role_id != 2:
                return {"seccess":False,"data":None,"Error":"You are Not Admin Or Not Super User"}
            query2 = select(Products).where(Products.id == model.product_id)
            res2 = await session.execute(query2)
            result2 = res2.scalar()
            if result2:
                if 0 < model.discount < 100:
                    new_price = (result2.price * (100 - model.discount)) / 100
                    query_insert = insert(SaleProducts).values(
                        product_id = model.product_id,
                        new_price = new_price,
                        sale = model.discount,
                        deadline = model.limit
                    )
                    await session.execute(query_insert)
                    await session.commit()
                    return {"success": True, "data": "Product added to SaleProduct", "Error": None}
                else:return {"success":False,"data":None,"Error":"Discount must be between 0 and 100"}
            else:return {"success":False , "data":None , "Error":"No Products"}
        else:return {"success":False , "data":None , "Error":"No Data"}

    except Exception as e:
        return {"success":False , "data":None , "Error":e}





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


@product.post("/product_addded_category/")
async def product_add_category(model:ProductAddCategory,
                               token:dict=Depends(verify_token),
                               session:AsyncSession = Depends(get_async_session)):

    try:
        user_id = token.get("user_id")
        query = select(User).where(User.id == user_id)
        res = await session.execute(query)
        result = res.scalar_one_or_none()

        if result:
            if result.role_id != 3 != result.role_id != 2:
                return {"success":False,"data":None,"Error":"You are Not Admin Or Not Super User"}
            query2 = select(Products).where(Products.id == product)
            query2 = insert(ProductCategory).values(product_id = model.product_id,
                                                    category_id = model.category_id)
            await session.execute(query2)
            await session.commit()
        return {"success":False,"data":None,"Error":"No Data"}

    except Exception as e:
        return {"Success": False, "Data": None, "Error": str(e)}