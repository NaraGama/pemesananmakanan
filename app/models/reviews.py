from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class ReviewBase(BaseModel):
    rating: int  # Rating antara 1-5
    komentar: str
    user_id: str  # ID pengguna yang memberikan ulasan
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ReviewRestoran(ReviewBase):
    restoran_id: str  # ID restoran yang diulas

class ReviewMenu(ReviewBase):
    menu_id: str  # ID menu yang diulas

# Untuk menangani ObjectId dari MongoDB
class ReviewInDB(ReviewBase):
    id: str
    class Config:
        json_encoders = {
            ObjectId: str
        }
