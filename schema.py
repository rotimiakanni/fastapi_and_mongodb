from typing import Optional
from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    description: str

class Book(BookBase):
    id: str
        
class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    description: Optional[str] = None

# User
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    full_name: str
    password: str

class UserInDB(UserBase):
    full_name: str
    hashed_password: str