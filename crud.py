#crud.py
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from fastapi import HTTPException, status

from database import (
    books_collection,
    users_collection
)
import schema
import serializer

class CRUDService:

    @staticmethod
    def create_book(book_data: schema.BookCreate):
        book_data = jsonable_encoder(book_data)
        book_document_data = books_collection.insert_one(
            book_data
        )
        book_id = book_document_data.inserted_id
        book_document = books_collection.find_one(
            {"_id": ObjectId(book_id)}
        )
        return serializer.book_serializer(book_document)
    
    @staticmethod
    def get_all_books(skip: int = 0, limit: int = 10):
        books = books_collection.find().skip(skip).limit(limit)
        return [serializer.book_serializer(book) for book in books]
    
    @staticmethod
    def get_book_by_id(book_id: str):
        book = books_collection.find_one({"_id": ObjectId(book_id)})
        if book:
            return serializer.book_serializer(book)
        return None
        

    @staticmethod
    def update_book(book_id: str, book_update_in: schema.BookUpdate):
        book = books_collection.find_one(
            {"_id": ObjectId(book_id)}
        )
        if not book:
            return None
        book_update_data = book_update_in.model_dump(exclude_unset=True)
        book_updated = books_collection.find_one_and_update(
            {"_id": ObjectId(book_id)}, {"$set": book_update_data}, return_document=True
        )
        return serializer.book_serializer(book_updated)
    
    @staticmethod
    def delete_book(book_id: str):
        return books_collection.find_one_and_delete({"_id": ObjectId(book_id)})
    

class UserCRUDService:
    @staticmethod
    def create_user(user_data: schema.UserCreate, hashed_password: str):
        # verify if user exists
        if users_collection.find_one({"username": user_data.username}):
            raise HTTPException(detail='User already exists', status_code=status.HTTP_400_BAD_REQUEST)
        # continue if user does not exist
        user_data = jsonable_encoder(user_data)
        user_document_data = users_collection.insert_one(
            {
                "username": user_data.get('username'),
                "full_name": user_data.get('full_name'),
                "hashed_password": hashed_password
            }
        )
        user_id = user_document_data.inserted_id
        user_document = users_collection.find_one(
            {"_id": ObjectId(user_id)}
        )
        return serializer.user_serializer(user_document)
    
    @staticmethod
    def get_user_by_username(username: str) -> schema.UserInDB:
        user = users_collection.find_one({"username": username})
        if user:
            return serializer.user_serializer(user)
        return None
    
    @staticmethod
    def get_user_by_username_with_hash(username: str) -> schema.UserInDB:
        user = users_collection.find_one({"username": username})
        print('====', user)
        if user:
            return serializer.user_serializer_password(user)
        return None

crud_service = CRUDService()
user_crud_service = UserCRUDService()