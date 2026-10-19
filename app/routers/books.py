
from typing import Annotated, Optional

from fastapi import APIRouter, Query, status

from app.database import _check_isbn_unique, _get_or_404, _now, db
from app.schema import Book, BookCreate, BookPatch, ErrorResponse



router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", include_in_schema=False)
def root() -> dict:
    return {"message": "Books API en ligne. Documentation sur /docs"}
 
 
@router.get("/books", response_model=list[Book], tags=["Books"],
         summary="Lister / filtrer les livres")
def list_books(
    title: Annotated[Optional[str], Query(description="Contient (insensible à la casse)")] = None,
    author: Annotated[Optional[str], Query(description="Contient (insensible à la casse)")] = None,
    genre: Annotated[Optional[str], Query(description="Correspondance exacte (insensible à la casse)")] = None,
    year: Annotated[Optional[int], Query(ge=1000, le=2100)] = None,
    min_year: Annotated[Optional[int], Query(ge=1000, le=2100)] = None,
    max_year: Annotated[Optional[int], Query(ge=1000, le=2100)] = None,
    available: Optional[bool] = None,
    skip: Annotated[int, Query(ge=0, description="Décalage (pagination)")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Taille de page")] = 10,
):
    results = list(db.values())
    if title:
        results = [b for b in results if title.lower() in b.title.lower()]
    if author:
        results = [b for b in results if author.lower() in b.author.lower()]
    if genre:
        results = [b for b in results if b.genre and b.genre.lower() == genre.lower()]
    if year is not None:
        results = [b for b in results if b.year == year]
    if min_year is not None:
        results = [b for b in results if b.year >= min_year]
    if max_year is not None:
        results = [b for b in results if b.year <= max_year]
    if available is not None:
        results = [b for b in results if b.available == available]
    return results[skip: skip + limit]
 
 
@router.get("/books/{book_id}", response_model=Book, tags=["Books"],
         responses={404: {"model": ErrorResponse}}, summary="Obtenir un livre")
def get_book(book_id: int):
    return _get_or_404(book_id)
 
 
@router.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED,
          tags=["Books"], responses={409: {"model": ErrorResponse}},
          summary="Créer un livre")
def create_book(payload: BookCreate):
    global _next_id
    _check_isbn_unique(payload.isbn)
    now = _now()
    book = Book(id=_next_id, created_at=now, updated_at=now, **payload.model_dump())
    db[book.id] = book
    _next_id += 1
    return book
 
 
@router.put("/books/{book_id}", response_model=Book, tags=["Books"],
         responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
         summary="Remplacer un livre (complet)")
def update_book(book_id: int, payload: BookCreate):
    current = _get_or_404(book_id)
    _check_isbn_unique(payload.isbn, ignore_id=book_id)
    updated = Book(
        id=book_id,
        created_at=current.created_at,
        updated_at=_now(),
        **payload.model_dump(),
    )
    db[book_id] = updated
    return updated
 
 
@router.patch("/books/{book_id}", response_model=Book, tags=["Books"],
           responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
           summary="Modifier partiellement un livre")
def patch_book(book_id: int, payload: BookPatch):
    current = _get_or_404(book_id)
    changes = payload.model_dump(exclude_unset=True)
    if "isbn" in changes:
        _check_isbn_unique(changes["isbn"], ignore_id=book_id)
    updated = current.model_copy(update={**changes, "updated_at": _now()})
    db[book_id] = updated
    return updated
 
 
@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT,
            tags=["Books"], responses={404: {"model": ErrorResponse}},
            summary="Supprimer un livre")
def delete_book(book_id: int):
    _get_or_404(book_id)
    del db[book_id]
 