from typing import Optional
from pydantic import BaseModel

# Book Schemas
class BookBase(BaseModel):
    title: str
    author: str
    description: str

class Book(BookBase):
    id: str

class BookCreate(BookBase):
    user_id: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    full_name: str
    password: str

class UserInDB(UserBase):
    id: str
    full_name: str
    hashed_password: str

class User(UserBase):
    id: str
    full_name: str
