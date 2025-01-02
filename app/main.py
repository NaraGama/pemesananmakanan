from fastapi import FastAPI
from app.api import auth, users, restaurants, menus, orders, reviews

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
app.include_router(menus.router, prefix="/menus", tags=["menus"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])

@app.get("/")
async def root():
    return {"message": "Selamat datang di sistem pemesanan makanan!"}
