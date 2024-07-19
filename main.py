from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from crud import crud_service, user_crud_service
import schema
from auth import pwd_context, authenticate_user, create_access_token, get_current_user

app = FastAPI()

@app.post("/signup", tags=["Auth Endpoints"])
def signup(user: schema.UserCreate):
    db_user = user_crud_service.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    return user_crud_service.create_user(user_data=user, hashed_password=hashed_password)

@app.post("/login", tags=["Auth Endpoints"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.get('username')})
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.get('id')}

@app.post("/books", tags=["Book Endpoints"])
def create_book(book_data: schema.BookCreatePayload, user: schema.User = Depends(get_current_user)):
    book_data_u = schema.BookCreate(**book_data.model_dump(), user_id=user.get('id'))
    book = crud_service.create_book(book_data_u)
    return {"message": "Book created successfully!", "data": book}

@app.get("/books", tags=["Book Endpoints"])
def get_all_books(skip: int = 0, limit: int = 10, user: schema.User = Depends(get_current_user)):
    books = crud_service.get_all_books(skip, limit)
    return {"data": books}

@app.get("/books/{book_id}", tags=["Book Endpoints"])
def get_book_by_id(book_id: str, user: schema.User = Depends(get_current_user)):
    book = crud_service.get_book_by_id(book_id)
    if not book:
        return {"message": "Book not found"}
    return {"data": book}

@app.put("/books/{book_id}", tags=["Book Endpoints"])
def update_book(book_id: str, book_data: schema.BookUpdate, user: schema.User = Depends(get_current_user)):
    book = crud_service.update_book(book_id, book_data, user.get('id'))
    if not book:
        raise HTTPException(detail="Book not found", status_code=status.HTTP_400_BAD_REQUEST)
    return {"message": "Book updated successfully!", "data": book}

@app.delete("/books/{book_id}", tags=["Book Endpoints"],)
def delete_book(book_id: str, user: schema.User = Depends(get_current_user)):
    result = crud_service.delete_book(book_id, user.get('id'))
    if not result:
        raise HTTPException(detail="Book not found or not in your collections", status_code=status.HTTP_400_BAD_REQUEST)
    return {"message": "Book deleted successfully!"}

@app.get("/user/books", tags=["Book Endpoints"])
def get_user_books(user: schema.User = Depends(get_current_user), skip: int =0, limit: int =10):
    books = crud_service.get_books_by_user_id(user.get('id'), skip=skip, limit=limit)
    if not books:
        return {"message": "No book available, create one"}
    return {"data": books}