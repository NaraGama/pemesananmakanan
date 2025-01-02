from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    nama: str
    email: str
    nomor_telepon: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str
