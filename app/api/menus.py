from fastapi import APIRouter, HTTPException
from app.database import db
from app.models.menus import Menu, MenuInDB
from app.schemas.menus import MenuCreate, MenuUpdate
from typing import List
from bson import ObjectId  # Import ObjectId untuk konversi
from datetime import datetime

router = APIRouter()

# Fungsi untuk mengonversi ObjectId menjadi string
def str_object_id(id):
    return str(id) if isinstance(id, ObjectId) else id

# Daftar menu berdasarkan restoran
@router.get("/menus/{restoran_id}", response_model=List[MenuInDB])
async def get_menus(restoran_id: str):
    menus = await db.menus.find({"restoran_id": restoran_id}).to_list(100)
    # Pastikan ObjectId diubah ke string
    return [MenuInDB(**{**menu, 'id': str_object_id(menu['_id'])}) for menu in menus]

# Detail menu berdasarkan ID
@router.get("/menus/detail/{menu_id}", response_model=MenuInDB)
async def get_menu_detail(menu_id: str):
    menu = await db.menus.find_one({"_id": ObjectId(menu_id)})
    if not menu:
        raise HTTPException(status_code=404, detail="Menu tidak ditemukan")
    
    # Mengonversi ObjectId ke string
    menu['id'] = str_object_id(menu['_id'])
    menu.pop('_id')  # Menghapus _id agar tidak muncul dalam response
    return MenuInDB(**menu)

# Menambah menu baru
@router.post("/menus", response_model=MenuInDB)
async def create_menu(menu: MenuCreate):
    restoran = await db.restaurants.find_one({"_id": ObjectId(menu.restoran_id)})
    if not restoran:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")
    
    # Menambahkan data menu
    menu_data = menu.dict()
    result = await db.menus.insert_one(menu_data)
    new_menu = await db.menus.find_one({"_id": result.inserted_id})

    # Mengonversi ObjectId menjadi string sebelum mengembalikan response
    new_menu['id'] = str_object_id(new_menu['_id'])
    new_menu.pop('_id')  # Menghapus _id agar tidak muncul dalam response
    
    return MenuInDB(**new_menu)

# Update menu
@router.put("/menus/{menu_id}", response_model=MenuInDB)
async def update_menu(menu_id: str, menu_update: MenuUpdate):
    existing_menu = await db.menus.find_one({"_id": ObjectId(menu_id)})
    if not existing_menu:
        raise HTTPException(status_code=404, detail="Menu tidak ditemukan")

    update_data = menu_update.dict(exclude_unset=True)
    result = await db.menus.update_one(
        {"_id": ObjectId(menu_id)}, {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Gagal memperbarui menu")

    updated_menu = await db.menus.find_one({"_id": ObjectId(menu_id)})
    updated_menu['id'] = str_object_id(updated_menu['_id'])
    updated_menu.pop('_id')  # Menghapus _id agar tidak muncul dalam response
    return MenuInDB(**updated_menu)

# Hapus menu
@router.delete("/menus/{menu_id}", response_model=MenuInDB)
async def delete_menu(menu_id: str):
    existing_menu = await db.menus.find_one({"_id": ObjectId(menu_id)})
    if not existing_menu:
        raise HTTPException(status_code=404, detail="Menu tidak ditemukan")

    await db.menus.delete_one({"_id": ObjectId(menu_id)})
    existing_menu['id'] = str_object_id(existing_menu['_id'])
    existing_menu.pop('_id')  # Menghapus _id agar tidak muncul dalam response
    return MenuInDB(**existing_menu)
