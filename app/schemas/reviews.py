from pydantic import BaseModel
from typing import List, Optional

class ReviewBase(BaseModel):
    rating: int  # Rating antara 1-5
    komentar: str

class ReviewRestoranResponse(ReviewBase):
    user_id: str
    created_at: str

class ReviewMenuResponse(ReviewBase):
    user_id: str
    created_at: str

class ReviewResponse(BaseModel):
    restoran_ulasans: List[ReviewRestoranResponse] = []
    menu_ulasans: List[ReviewMenuResponse] = []
