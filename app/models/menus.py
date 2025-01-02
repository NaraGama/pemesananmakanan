from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from typing import Optional

class Menu(BaseModel):
    id: str  # Gunakan str untuk ID agar dapat menampung ObjectId yang sudah diubah
    nama: str
    harga: int
    deskripsi: Optional[str] = None
    gambar_url: Optional[str] = None
    restoran_id: str  # Relasi ke restoran

class MenuInDB(BaseModel):
    id: str  # Menggunakan string untuk id
    nama: str
    harga: int
    deskripsi: Optional[str] = None
    gambar_url: Optional[str] = None
    restoran_id: str

    class Config:
        # Menambahkan alias untuk _id MongoDB
        json_encoders = {
            ObjectId: str  # Mengonversi ObjectId menjadi string saat serialisasi
        }