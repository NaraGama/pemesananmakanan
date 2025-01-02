from fastapi import APIRouter, HTTPException
from app.database import db
from app.schemas.analytics import DashboardAdmin, StatistikPenjualan, MenuPalingLaris, PerformaRestoran
from typing import List

router = APIRouter()

# Dashboard Admin untuk menampilkan analitik
@router.get("/dashboard", response_model=DashboardAdmin)
async def get_dashboard_admin():
    # Statistik Penjualan
    total_pendapatan = 0
    jumlah_pesanan = 0
    orders = await db.orders.find({"status": "Selesai"}).to_list(100)  # Mengambil semua pesanan selesai
    for order in orders:
        total_pendapatan += order['total_harga']
        jumlah_pesanan += 1

    statistik_penjualan = StatistikPenjualan(
        total_pendapatan=total_pendapatan,
        jumlah_pesanan=jumlah_pesanan
    )

    # Menu Paling Laris
    menu_sales = {}
    for order in orders:
        for item in order['items']:
            if item['menu_id'] in menu_sales:
                menu_sales[item['menu_id']]['jumlah_terjual'] += item['jumlah']
                menu_sales[item['menu_id']]['total_pendapatan'] += item['total_harga']
            else:
                menu_sales[item['menu_id']] = {
                    'nama_menu': item['nama'],
                    'jumlah_terjual': item['jumlah'],
                    'total_pendapatan': item['total_harga']
                }

    menu_paling_laris = [MenuPalingLaris(
        menu_id=menu_id,
        nama_menu=menu_data['nama_menu'],
        jumlah_terjual=menu_data['jumlah_terjual'],
        total_pendapatan=menu_data['total_pendapatan']
    ) for menu_id, menu_data in menu_sales.items()]

    # Performa Restoran
    restoran_sales = {}
    for order in orders:
        restoran_id = order['restoran_id']
        if restoran_id in restoran_sales:
            restoran_sales[restoran_id]['jumlah_pesanan'] += 1
            restoran_sales[restoran_id]['total_pendapatan'] += order['total_harga']
        else:
            restoran = await db.restaurants.find_one({"_id": restoran_id})
            restoran_sales[restoran_id] = {
                'nama_restoran': restoran['nama'],
                'jumlah_pesanan': 1,
                'total_pendapatan': order['total_harga']
            }

    performa_restoran = [PerformaRestoran(
        restoran_id=restoran_id,
        nama_restoran=restoran_data['nama_restoran'],
        jumlah_pesanan=restoran_data['jumlah_pesanan'],
        total_pendapatan=restoran_data['total_pendapatan']
    ) for restoran_id, restoran_data in restoran_sales.items()]

    # Menyusun Dashboard Admin
    dashboard = DashboardAdmin(
        statistik_penjualan=statistik_penjualan,
        menu_paling_laris=menu_paling_laris,
        performa_restoran=performa_restoran
    )

    return dashboard
