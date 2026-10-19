
from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status

from app.schema import Book



db: dict[int, Book] = {}
_next_id = 1
 
 
def _now() -> datetime:
    return datetime.now(timezone.utc)
 
 
def _get_or_404(book_id: int) -> Book:
    book = db.get(book_id)
    if book is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Livre {book_id} introuvable"
        )
    return book
 
 
def _check_isbn_unique(isbn: str, ignore_id: Optional[int] = None) -> None:
    for b in db.values():
        if b.isbn == isbn and b.id != ignore_id:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=f"Un livre avec l'ISBN {isbn} existe déjà (id={b.id})",
            )
 
 