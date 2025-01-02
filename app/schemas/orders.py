from pydantic import BaseModel
from typing import List
from datetime import datetime
from bson import ObjectId

class OrderItem(BaseModel):
    menu_id: str
    nama: str
    jumlah: int
    harga: int
    total_harga: int

class OrderInDB(BaseModel):
    id: str  # id sebagai string untuk menampilkan _id dari database
    user_id: str
    restoran_id: str
    items: List[OrderItem]
    alamat_pengiriman: str
    metode_pembayaran: str
    total_harga: int
    status: str
    waktu_pemesanan: datetime

    class Config:
        # Mengkonversi ObjectId ke string saat serialisasi
        json_encoders = {
            ObjectId: str
        }


class OrderItemCreate(BaseModel):
    menu_id: str
    jumlah: int

class OrderCreate(BaseModel):
    user_id: str
    restoran_id: str
    items: List[OrderItemCreate]
    alamat_pengiriman: str
    metode_pembayaran: str
