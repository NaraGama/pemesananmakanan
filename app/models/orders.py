from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class OrderItem(BaseModel):
    menu_id: str  # ID menu yang dipesan
    nama: str
    jumlah: int
    harga: int
    total_harga: float  # Pastikan menggunakan float untuk total_harga

class Order(BaseModel):
    user_id: str
    restoran_id: str
    items: List[OrderItem]
    alamat_pengiriman: str
    metode_pembayaran: str  # Cash on delivery, e-wallet, kartu kredit
    total_harga: int  # Menggunakan int untuk total harga
    status: str  # Pending, Selesai, Dibatalkan
    waktu_pemesanan: datetime

class OrderInDB(BaseModel):
    _id: str  # Menggunakan str untuk _id, karena ObjectId perlu diubah menjadi string saat serialisasi
    user_id: str
    restoran_id: str
    items: List[OrderItem]
    alamat_pengiriman: str
    metode_pembayaran: str
    total_harga: int
    status: str  # Pending, Selesai, Dibatalkan
    waktu_pemesanan: datetime

    class Config:
        # Mengonversi ObjectId ke string saat serialisasi JSON
        json_encoders = {
            ObjectId: str
        }
