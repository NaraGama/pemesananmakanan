from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.database import db
from app.models.restaurant import Restaurant, RestaurantInDB
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from typing import List

router = APIRouter()

# Helper function to convert MongoDB _id to id
def convert_mongo_id(document):
    document["id"] = str(document.pop("_id"))
    return document

# Daftar restoran
@router.get("/restaurants", response_model=List[RestaurantInDB])
async def get_restaurants():
    restaurants = await db.restaurants.find().to_list(100)
    return [RestaurantInDB(**convert_mongo_id(restaurant)) for restaurant in restaurants]

# Detail restoran berdasarkan ID
@router.get("/restaurants/{restaurant_id}", response_model=RestaurantInDB)
async def get_restaurant_detail(restaurant_id: str):
    if not ObjectId.is_valid(restaurant_id):
        raise HTTPException(status_code=400, detail="ID tidak valid")
    restaurant = await db.restaurants.find_one({"_id": ObjectId(restaurant_id)})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")
    return RestaurantInDB(**convert_mongo_id(restaurant))

# Tambah restoran (Admin)
@router.post("/restaurants", response_model=RestaurantInDB)
async def create_restaurant(restaurant: RestaurantCreate):
    restaurant_data = restaurant.dict()
    result = await db.restaurants.insert_one(restaurant_data)
    new_restaurant = await db.restaurants.find_one({"_id": result.inserted_id})
    return RestaurantInDB(**convert_mongo_id(new_restaurant))

# Update restoran (Admin)
@router.put("/restaurants/{restaurant_id}", response_model=RestaurantInDB)
async def update_restaurant(restaurant_id: str, restaurant_update: RestaurantUpdate):
    if not ObjectId.is_valid(restaurant_id):
        raise HTTPException(status_code=400, detail="ID tidak valid")
    existing_restaurant = await db.restaurants.find_one({"_id": ObjectId(restaurant_id)})
    if not existing_restaurant:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")

    update_data = restaurant_update.dict(exclude_unset=True)
    result = await db.restaurants.update_one(
        {"_id": ObjectId(restaurant_id)}, {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Gagal memperbarui restoran")

    updated_restaurant = await db.restaurants.find_one({"_id": ObjectId(restaurant_id)})
    return RestaurantInDB(**convert_mongo_id(updated_restaurant))

# Hapus restoran (Admin)
@router.delete("/restaurants/{restaurant_id}", response_model=RestaurantInDB)
async def delete_restaurant(restaurant_id: str):
    if not ObjectId.is_valid(restaurant_id):
        raise HTTPException(status_code=400, detail="ID tidak valid")
    existing_restaurant = await db.restaurants.find_one({"_id": ObjectId(restaurant_id)})
    if not existing_restaurant:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")

    await db.restaurants.delete_one({"_id": ObjectId(restaurant_id)})
    return RestaurantInDB(**convert_mongo_id(existing_restaurant))
