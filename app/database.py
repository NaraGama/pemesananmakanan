from dotenv import load_dotenv
import os

# Muat file .env secara eksplisit (pastikan path-nya benar)
load_dotenv(dotenv_path="E:/AjiMaulana/tugas/backend_pemeasanan_makanan/app/.env")

# Ambil variabel dari environment
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

print(f"MONGO_URI: {MONGO_URI}")
print(f"MONGO_DB: {MONGO_DB}")

# Validasi bahwa MONGO_DB bertipe string
if not isinstance(MONGO_DB, str):
    raise ValueError("MONGO_DB harus bertipe string")

# Membuat koneksi ke database
from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]
