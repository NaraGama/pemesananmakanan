import os
from dotenv import load_dotenv

# Memuat variabel dari file .env
load_dotenv()

# Mengambil variabel lingkungan dari file .env
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
SECRET_KEY = os.getenv("SECRET_KEY")

# Memastikan nilai yang diambil tidak kosong
if not MONGO_URI:
    raise ValueError("MONGO_URI is missing from the .env file")
if not MONGO_DB:
    raise ValueError("MONGO_DB is missing from the .env file")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing from the .env file")

# Variabel konfigurasi yang dapat diimpor ke file lain
config = {
    "MONGO_URI": MONGO_URI,
    "MONGO_DB": MONGO_DB,
    "SECRET_KEY": SECRET_KEY
}
