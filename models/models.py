from sqlalchemy import String, Integer, Column, MetaData, DATE, Text, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

metadata = MetaData()
Base = declarative_base(metadata=metadata)




class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,autoincrement=True)
    firstname = Column(String,nullable=True)
    lastname = Column(String,nullable=True)
    username = Column(String,unique=True,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    registred_date = Column(DATE,default=datetime.utcnow)
    is_admin = Column(Boolean,default = False)



class Products(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key = True,autoincrement=True)
    user_id = Column(ForeignKey("users.id"))
    name = Column(String,nullable=False)
    description = Column(Text,nullable=True)
    price = Column(Float,nullable=False)
    count = Column(Integer)
    joined_date = Column(DATE,default=datetime.utcnow)
    rating = Column(Integer,default=5)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer,primary_key=True,autoincrement=True)
    category = Column(String,unique=True,nullable=False)


class ProductCategory(Base):
    __tablename__ =  "product_category"

    id = Column(Integer,primary_key=True,autoincrement=True)
    category_id = Column(Integer,ForeignKey("category.id"))
    product_id = Column(Integer,ForeignKey("products.id"))