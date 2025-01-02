from fastapi import APIRouter, HTTPException, Depends
from app.database import db
from app.schemas.reviews import ReviewRestoranResponse, ReviewMenuResponse
from app.models.reviews import ReviewRestoran, ReviewMenu, ReviewInDB
from typing import List
from bson import ObjectId

router = APIRouter()

# Menambahkan Ulasan Restoran
@router.post("/reviews/restoran", response_model=ReviewRestoranResponse)
async def add_restaurant_review(review: ReviewRestoran):
    # Menyimpan ulasan restoran ke database
    restoran = await db.restaurants.find_one({"_id": ObjectId(review.restoran_id)})
    if not restoran:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")
    
    review_in_db = ReviewInDB(
        rating=review.rating,
        komentar=review.komentar,
        user_id=review.user_id,
        restoran_id=review.restoran_id,
        created_at=review.created_at
    )
    
    result = await db.reviews_restoran.insert_one(review_in_db.dict())
    review_in_db.id = str(result.inserted_id)
    return review_in_db

# Menambahkan Ulasan Menu
@router.post("/reviews/menu", response_model=ReviewMenuResponse)
async def add_menu_review(review: ReviewMenu):
    # Menyimpan ulasan menu ke database
    menu = await db.menus.find_one({"_id": ObjectId(review.menu_id)})
    if not menu:
        raise HTTPException(status_code=404, detail="Menu tidak ditemukan")
    
    review_in_db = ReviewInDB(
        rating=review.rating,
        komentar=review.komentar,
        user_id=review.user_id,
        menu_id=review.menu_id,
        created_at=review.created_at
    )
    
    result = await db.reviews_menu.insert_one(review_in_db.dict())
    review_in_db.id = str(result.inserted_id)
    return review_in_db

# Mendapatkan Ulasan Restoran
@router.get("/reviews/restoran/{restoran_id}", response_model=List[ReviewRestoranResponse])
async def get_restaurant_reviews(restoran_id: str):
    reviews = await db.reviews_restoran.find({"restoran_id": restoran_id}).to_list(100)
    return [ReviewRestoranResponse(
        rating=review['rating'],
        komentar=review['komentar'],
        user_id=review['user_id'],
        created_at=review['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    ) for review in reviews]

# Mendapatkan Ulasan Menu
@router.get("/reviews/menu/{menu_id}", response_model=List[ReviewMenuResponse])
async def get_menu_reviews(menu_id: str):
    reviews = await db.reviews_menu.find({"menu_id": menu_id}).to_list(100)
    return [ReviewMenuResponse(
        rating=review['rating'],
        komentar=review['komentar'],
        user_id=review['user_id'],
        created_at=review['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    ) for review in reviews]
