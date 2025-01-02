from app.database import db

async def blacklist_token(token: str):
    await db.blacklist.insert_one({"token": token})
    
async def is_token_blacklisted(token: str) -> bool:
    blacklist_entry = await db.blacklist.find_one({"token": token})
    return blacklist_entry is not None
