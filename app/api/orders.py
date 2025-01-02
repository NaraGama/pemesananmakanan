from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.database import db
from app.models.orders import Order, OrderInDB, OrderItem
from app.schemas.orders import OrderCreate
from datetime import datetime
from typing import List

router = APIRouter()

def str_to_objectid(id: str):
    if ObjectId.is_valid(id):
        return ObjectId(id)
    raise HTTPException(status_code=400, detail="Invalid ID format")

# Menambah item ke keranjang belanja
@router.post("/keranjang/{user_id}/{menu_id}")
async def add_to_cart(user_id: str, menu_id: str, jumlah: int):
    menu_id = str_to_objectid(menu_id)
    menu = await db.menus.find_one({"_id": menu_id})
    if not menu:
        raise HTTPException(status_code=404, detail="Menu tidak ditemukan")

    keranjang = await db.carts.find_one({"user_id": user_id})
    if keranjang:
        existing_item = next((item for item in keranjang['items'] if item['menu_id'] == str(menu_id)), None)
        if existing_item:
            existing_item['jumlah'] += jumlah
            existing_item['total_harga'] = existing_item['jumlah'] * menu['harga']
        else:
            keranjang['items'].append({
                "menu_id": str(menu_id),
                "nama": menu['nama'],
                "jumlah": jumlah,
                "harga": menu['harga'],
                "total_harga": menu['harga'] * jumlah
            })
        await db.carts.update_one({"user_id": user_id}, {"$set": {"items": keranjang['items']}})
    else:
        new_cart = {
            "user_id": user_id,
            "items": [{
                "menu_id": str(menu_id),
                "nama": menu['nama'],
                "jumlah": jumlah,
                "harga": menu['harga'],
                "total_harga": menu['harga'] * jumlah
            }]
        }
        await db.carts.insert_one(new_cart)

    return {"message": "Item berhasil ditambahkan ke keranjang"}

# Mengedit jumlah item di keranjang
@router.put("/keranjang/{user_id}/{menu_id}")
async def update_cart(user_id: str, menu_id: str, jumlah: int):
    menu_id = str_to_objectid(menu_id)
    keranjang = await db.carts.find_one({"user_id": user_id})
    if not keranjang:
        raise HTTPException(status_code=404, detail="Keranjang tidak ditemukan")

    item = next((item for item in keranjang['items'] if item['menu_id'] == str(menu_id)), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item tidak ditemukan dalam keranjang")

    menu = await db.menus.find_one({"_id": menu_id})
    if not menu:
        raise HTTPException(status_code=404, detail="Menu tidak ditemukan")

    item['jumlah'] = jumlah
    item['total_harga'] = jumlah * menu['harga']
    await db.carts.update_one({"user_id": user_id}, {"$set": {"items": keranjang['items']}})

    return {"message": "Jumlah item dalam keranjang berhasil diperbarui"}

# Menghapus item dari keranjang
@router.delete("/keranjang/{user_id}/{menu_id}")
async def delete_from_cart(user_id: str, menu_id: str):
    menu_id = str_to_objectid(menu_id)
    keranjang = await db.carts.find_one({"user_id": user_id})
    if not keranjang:
        raise HTTPException(status_code=404, detail="Keranjang tidak ditemukan")

    keranjang['items'] = [item for item in keranjang['items'] if item['menu_id'] != str(menu_id)]
    await db.carts.update_one({"user_id": user_id}, {"$set": {"items": keranjang['items']}})

    return {"message": "Item berhasil dihapus dari keranjang"}

@router.post("/checkout", response_model=OrderInDB)
async def checkout(order: OrderCreate):
    total_harga = 0
    items = []
    
    for item in order.items:
        menu_id = str_to_objectid(item.menu_id)
        menu = await db.menus.find_one({"_id": menu_id})
        if not menu:
            raise HTTPException(status_code=404, detail=f"Menu dengan ID {item.menu_id} tidak ditemukan")
        total_harga += menu['harga'] * item.jumlah
        items.append(OrderItem(
            menu_id=str(menu_id),
            nama=menu['nama'],
            jumlah=item.jumlah,
            harga=menu['harga'],
            total_harga=menu['harga'] * item.jumlah
        ).dict())

    new_order = {
        "user_id": order.user_id,
        "restoran_id": order.restoran_id,
        "items": items,
        "alamat_pengiriman": order.alamat_pengiriman,
        "metode_pembayaran": order.metode_pembayaran,
        "total_harga": total_harga,
        "status": "Pending",
        "waktu_pemesanan": datetime.utcnow()
    }

    result = await db.orders.insert_one(new_order)
    new_order["_id"] = str(result.inserted_id)  # Mengubah ObjectId menjadi string

    return OrderInDB(**new_order)

# Riwayat pesanan
@router.get("/riwayat/{user_id}", response_model=List[OrderInDB])
async def get_order_history(user_id: str):
    orders = await db.orders.find({"user_id": user_id}).to_list(100)
    return [OrderInDB(**order) for order in orders]
