from pydantic import BaseModel
from typing import List, Optional

class Restaurant(BaseModel):
    nama: str
    alamat: str

class Restaurant(BaseModel):
    nama: str
    alamat: str
    jam_operasional: str
    rating: Optional[float] = None

class RestaurantInDB(Restaurant):
    id: str