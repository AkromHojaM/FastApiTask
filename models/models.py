# from sqlalchemy import String, Integer, Column, MetaData, DATE, Text, Float, ForeignKey, Boolean
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime
#
# from sqlalchemy.orm import relationship
#
# metadata = MetaData()
# Base = declarative_base(metadata=metadata)
#
#
#
#
# class Role(Base):
#     __tablename__ = "role"
#
#     id = Column(Integer,primary_key=True,autoincrement=True)
#     name = Column(String)
#
#     users = relationship("User",back_populates="role")
#
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer,primary_key=True,autoincrement=True)
#     firstname = Column(String,nullable=True)
#     lastname = Column(String,nullable=True)
#     username = Column(String,unique=True,nullable=False)
#     email = Column(String,unique=True,nullable=False)
#     password = Column(String,nullable=False)
#     registred_date = Column(DATE,default=datetime.utcnow)
#     is_admin = Column(Boolean,default = False)
#     role_id = Column(Integer,ForeignKey("role.id"))
#
#
#     role = relationship("Role",back_populates="users")
#     rating = relationship("Rating",back_populates="users")
#     products = relationship("Products",back_populates="users")
#
#
#
# class Rating(Base):
#     __tablename__ = "rating"
#
#     id = Column(Integer,primary_key = True,autoincrement=True)
#     user_id = Column(Integer,ForeignKey("users.id"))
#     product_id = Column(Integer,ForeignKey("products.id"))
#     rate = Column(Integer,default =5)
#
#
#     users = relationship("User",back_populates="rating")
#     products = relationship("Products",back_populates="rate")
#
#
#
# class Products(Base):
#     __tablename__ = "products"
#
#     id = Column(Integer,primary_key = True,autoincrement=True)
#     user_id = Column(ForeignKey("users.id"))
#     name = Column(String,nullable=False)
#     description = Column(Text,nullable=True)
#     price = Column(Float,nullable=False)
#     count = Column(Integer)
#     joined_date = Column(DATE,default=datetime.utcnow)
#     rating = Column(Integer,default=5)
#
#
#     users = relationship("User",back_populates="products")
#     product_category = relationship("ProductCategory",back_populates="products")
#     sale_products = relationship("SaleProducts",back_populates="products")
#     rate = relationship("Rating",back_populates="products")
#
#
#
# class Category(Base):
#     __tablename__ = "category"
#
#     id = Column(Integer,primary_key=True,autoincrement=True)
#     category = Column(String,unique=True,nullable=False)
#
#
#     category_products = relationship("ProductCategory",back_populates="category")
#
#
# class ProductCategory(Base):
#     __tablename__ =  "product_category"
#
#     id = Column(Integer,primary_key=True,autoincrement=True)
#     category_id = Column(Integer,ForeignKey("category.id"))
#     product_id = Column(Integer,ForeignKey("products.id"))
#
#
#     products = relationship("Products",back_populates="product_category")
#     category = relationship("Category",back_populates="product_category")
#
#
# class SaleProducts(Base):
#     __tablename__ = "sale_products"
#
#     id = Column(Integer,primary_key=True,autoincrement=True)
#     product_id = Column(Integer,ForeignKey("products.id"))
#     new_price = Column(Float)
#     sale = Column(Integer)
#     joined_date = Column(DATE,default=datetime.utcnow)
#     deadline = Column(Integer,default=7)
#
#
#     products = relationship("Products",back_populates="sale_products")
from sqlalchemy import String, Integer, Column, MetaData, DATE, Text, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    registred_date = Column(DATE, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("role.id"))

    role = relationship("Role", back_populates="users")
    rating = relationship("Rating", back_populates="user")
    products = relationship("Products", back_populates="user")


class Rating(Base):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    rate = Column(Integer, default=5)

    user = relationship("User", back_populates="rating")
    product = relationship("Products", back_populates="ratings")


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    count = Column(Integer)
    joined_date = Column(DATE, default=datetime.utcnow)
    rating = Column(Integer, default=5)

    user = relationship("User", back_populates="products")
    product_category = relationship("ProductCategory", back_populates="product")
    sale_products = relationship("SaleProducts", back_populates="product")
    ratings = relationship("Rating", back_populates="product")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, unique=True, nullable=False)

    product_categories = relationship("ProductCategory", back_populates="category")


class ProductCategory(Base):
    __tablename__ = "product_category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    product = relationship("Products", back_populates="product_category")
    category = relationship("Category", back_populates="product_categories")


class SaleProducts(Base):
    __tablename__ = "sale_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    new_price = Column(Float)
    sale = Column(Integer)
    joined_date = Column(DATE, default=datetime.utcnow)
    deadline = Column(Integer, default=7)

    product = relationship("Products", back_populates="sale_products")
