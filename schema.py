from typing import Optional
from pydantic import BaseModel

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
    user_id: str
    description: Optional[str] = None

class BookDelete(BookBase):
    user_id: str
    
    
# User
class UserBase(BaseModel):
    id: str
    username: str

class UserCreate(UserBase):
    full_name: str
    password: str

class UserInDB(UserBase):
    full_name: str
    hashed_password: str
    
class user(UserBase):
    full_name: str
    
