from pydantic import BaseModel
from typing import List

class StatistikPenjualan(BaseModel):
    total_pendapatan: float
    jumlah_pesanan: int

class MenuPalingLaris(BaseModel):
    menu_id: str
    nama_menu: str
    jumlah_terjual: int
    total_pendapatan: float

class PerformaRestoran(BaseModel):
    restoran_id: str
    nama_restoran: str
    jumlah_pesanan: int
    total_pendapatan: float

class DashboardAdmin(BaseModel):
    statistik_penjualan: StatistikPenjualan
    menu_paling_laris: List[MenuPalingLaris]
    performa_restoran: List[PerformaRestoran]
