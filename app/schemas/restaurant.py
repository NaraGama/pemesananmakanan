from pydantic import BaseModel
from typing import List, Optional

class RestaurantCreate(BaseModel):
    nama: str
    alamat: str
    jam_operasional: str
    rating: Optional[float] = None

class RestaurantUpdate(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    menu: Optional[List[str]] = None
    jam_operasional: Optional[str] = None
    rating: Optional[float] = None