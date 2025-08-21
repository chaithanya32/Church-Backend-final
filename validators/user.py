# validators/user.py
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    id_number: Optional[str] = None
    batch: Optional[str] = None
    branch: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
