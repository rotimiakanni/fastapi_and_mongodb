from fastapi import FastAPI,HTTPException, status, Depends
import schemas
from crud import crud_service, user_crud_service
from auth import pwd_context, authenticate_user, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm


app = FastAPI()



@app.post("/signup")
def signup(user: schemas.UserCreate):
    db_user = user_crud_service.get_user_by_username(username=user.username)
    hashed_password = pwd_context.hash(user.password)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return user_crud_service.create_user(user_data=user, hashed_password=hashed_password)


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate" : "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.get("username")})
    return {"access_token": access_token, "token_type": "bearer"}

# ------------------------------------------------------------


@app.post("/books")
def create_book(book_data: schemas.BookCreate, user: schemas.UserBase = Depends(get_current_user)):
    book = crud_service.create_book(book_data, user_id=user.get("id"))
    return {"message": "Book created successfully!", "data": book}


@app.get("/books/user")
def get_book_for_user(user: schemas.UserBase = Depends(get_current_user), skip: int =0, limit: int =10):
    books = crud_service.get_books_by_user_id(
        user_id=user.get("id"),
        skip=skip,
        limit=limit
    )
    return {"message": "success", "data": books}





@app.get("/books")
def get_books(skip: int = 0, limit: int = 10):
    books = crud_service.get_all_books(skip, limit)
    return {"data": books}


# @app.get("/books/{book_id}")
# def get_book_by_id(book_id: str):
#     book = crud_service.get_book_by_id(book_id)
#     if not book:
#         return {"message": "Book not found"}
#     return {"data": book}




@app.put('/book_update/{book_id}')
def update_movie(book_id: str, book_payload: schemas.BookUpdate, user: schemas.UserInDB = Depends(get_current_user)):
    book = crud_service.update_book(book_id, book_payload, user_id=user.get("id"))
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    return {"message": "success", "data": book}




@app.delete("/books/{book_id}")
def delete_book(book_id: str, user: schemas.UserInDB = Depends(get_current_user)):
    deleted_book = crud_service.delete_book(book_id, user_id=user.get("id"))
    if not deleted_book:
        raise HTTPException(detail="Book not found", status_code=status.HTTP_400_BAD_REQUEST)
    return {"message": "Book deleted successfully!"}