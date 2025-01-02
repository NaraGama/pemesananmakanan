from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
import base64
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os
from app.database import db

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Fungsi untuk mengurai Basic Auth
def get_basic_auth_credentials(auth_header: str):
    if not auth_header.startswith("Basic "):
        raise HTTPException(status_code=400, detail="Invalid authorization code")
    
    encoded_credentials = auth_header[6:]
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
    username, password = decoded_credentials.split(":", 1)
    return username, password

@router.post("/login", response_model=Token)
async def login_for_access_token(request: Request):
    auth_header = request.headers.get("Authorization")
    
    if auth_header is None:
        raise HTTPException(status_code=400, detail="Authorization header missing")
    
    # Mengurai Basic Auth untuk mendapatkan email dan password
    email, password = get_basic_auth_credentials(auth_header)

    # Mencari pengguna berdasarkan email
    user = await db.users.find_one({"email": email})
    
    if user and pwd_context.verify(password, user["password"]):  # Memverifikasi password
        access_token = create_access_token(data={"sub": email})
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Email atau password salah")

# Fungsi untuk memeriksa apakah token sudah ada dalam blacklist
async def is_token_blacklisted(token: str):
    # Cek apakah token ada dalam koleksi blacklisted_tokens
    blacklisted_token = await db.blacklisted_tokens.find_one({"token": token})
    return blacklisted_token is not None

# Fungsi untuk menambahkan token ke blacklist
async def add_token_to_blacklist(token: str):
    # Menyimpan token yang diblacklist ke dalam database
    await db.blacklisted_tokens.insert_one({"token": token})

# Endpoint untuk logout
@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Cek apakah token sudah diblacklist
    if await is_token_blacklisted(token):
        raise HTTPException(status_code=400, detail="Token sudah di-logout sebelumnya")
    
    # Tambahkan token ke blacklist
    await add_token_to_blacklist(token)
    return {"message": "Logout sukses"}