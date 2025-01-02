from pydantic import BaseModel
from typing import Optional
from pydantic import root_validator

class User(BaseModel):
    nama: str
    email: str
    password: str

class UserInDB(BaseModel):
    id: Optional[str]  # Pastikan id adalah string
    nama: str
    email: str
    password: str

    @root_validator(pre=True)
    def convert_objectid_to_str(cls, values):
        if '_id' in values:
            values['id'] = str(values['_id'])
            del values['_id']  # Hapus _id setelah konversi
        return values