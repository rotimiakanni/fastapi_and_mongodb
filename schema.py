from typing import Optional
from pydantic import BaseModel
from bson.objectid import ObjectId

class BookBase(BaseModel):
    title: str
    author: str
    description: str

class Book(BookBase):
    id: str
        
class BookCreatePayload(BookBase):
    pass

class BookCreate(BookBase):
    user_id: str

class BookUpdate(BookBase):
    description: Optional[str] = None

# User
class UserBase(BaseModel):
    username: str
    full_name: str

class User(UserBase):
    id: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str
    hashed_password: str