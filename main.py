from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from crud import crud_service, user_crud_service
import schema
from auth import pwd_context, authenticate_user, create_access_token, get_current_user

app = FastAPI()

@app.post("/signup")
def signup(user: schema.UserCreate):
    db_user = user_crud_service.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    return user_crud_service.create_user(user_data=user, hashed_password=hashed_password)

@app.post("/login")
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

@app.post("/books")
def create_book(book_data: schema.BookCreate, user: schema.UserBase = Depends(get_current_user)):
    """
    ## Create a Book
    Done by an Authenticated User
    """
    book = crud_service.create_book(book_data)
    return {"message": "Book created successfully!", "data": book}

@app.get("/books")
def get_all_books(skip: int = 0, limit: int = 10, current_user : schema.UserBase = Depends(get_current_user)):
    """
    ## Fetch Books
    Done by an Authenticated User
    """
    books = crud_service.get_all_books(skip, limit)
    return {"data": books}

@app.get("/books/{book_id}")
def get_book_by_id(book_id: str,  current_user : schema.UserBase = Depends(get_current_user)):
    """
    ## Fetch Book by it's id
    Done by an Authenticated User that created the book and returns not Authorized if it is not the user making the request
    """
    book = crud_service.get_book_by_id(book_id)
    if not book:
            return {"message": "Book not found"}
    if current_user.get("id")== book.get("user_id"):
        return {"data": book}
    raise HTTPException (
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not authorized to access this resource"
    )
  

@app.put("/books/{book_id}")
def update_book(book_id: str, book_data: schema.BookUpdate, current_user : schema.UserBase = Depends(get_current_user)):
    """
    ## Update Book by it's id
    Done by an Authenticated User that created the book and returns not Authorized if it is not the user making the request
    """
    book = crud_service.get_book_by_id(book_id)
    if not book:
            return {"message": "Book not found"}
    if current_user.get("id")== book.get("user_id"):
        book = crud_service.update_book(book_id, book_data)
        return {"message": "Book updated successfully!", "data": book}
    raise HTTPException (
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not authorized to Update this resource"
    )    
 

@app.delete("/books/{book_id}")
def delete_book(book_id: str,  current_user : schema.UserBase = Depends(get_current_user)):
    """
    ## Delete Book by it's id
    Done by an Authenticated User that created the book and returns not Authorized if it is not the user making the request
    """
    book = crud_service.get_book_by_id(book_id)
    if not book:
            return {"message": "Book not found"}
    if current_user.get("id") == book.get("user_id"):
        crud_service.delete_book(book_id)
        return {"message": "Book deleted successfully!"}
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not authorized to delete this resource"
    )
   