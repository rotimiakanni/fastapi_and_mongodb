from typing import Dict

def book_serializer(book: dict) -> Dict[str, str]:
    """Converts a MongoDB book object to a Python dictionary."""
    return {
        "id": str(book.get("_id")),
        "title": book.get("title"),
        "author": book.get("author")),
        "description": book.get("description"),
        "user_id": str(book.get("user_id"))
    }

def user_serializer(user: dict) -> Dict[str, str]:
    """Converts a MongoDB user object to a Python dictionary without password."""
    return {
        "id": str(user.get("_id")),
        "username": user.get("username"),
        "full_name": user.get("full_name")
    }

def user_serializer_password(user: dict) -> Dict[str, str]:
    """Converts a MongoDB user object to a Python dictionary with password."""
    return {
        "id": str(user.get("_id")),
        "username": user.get("username"),
        "full_name": user.get("full_name"),
        "hashed_password": user.get("hashed_password")
    }
