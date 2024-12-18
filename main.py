from fastapi import APIRouter, FastAPI
from products.product import product
from authenticated.auth import user


app = FastAPI(title="Project")
app.include_router(user)
app.include_router(product)