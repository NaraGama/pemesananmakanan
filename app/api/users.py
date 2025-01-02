from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.database import db
from passlib.context import CryptContext
from app.schemas.user import UserCreate
from app.models.user import UserInDB

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserInDB)
async def register_user(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    
    hashed_password = pwd_context.hash(user.password)
    user_data = {**user.dict(), "password": hashed_password}
    result = await db.users.insert_one(user_data)
    new_user = await db.users.find_one({"_id": result.inserted_id})
    return UserInDB(**new_user)
