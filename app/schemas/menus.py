from pydantic import BaseModel
from typing import Optional

class MenuCreate(BaseModel):
    nama: str
    harga: int
    deskripsi: Optional[str] = None
    gambar_url: Optional[str] = None
    restoran_id: str  # Relasi ke restoran

class MenuUpdate(BaseModel):
    nama: Optional[str] = None
    harga: Optional[int] = None
    deskripsi: Optional[str] = None
    gambar_url: Optional[str] = None
