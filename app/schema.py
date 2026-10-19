
from pydantic import BaseModel, ConfigDict, Field

from typing import Annotated, Optional
from datetime import datetime


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, examples=["Clean Code"])
    author: str = Field(..., min_length=1, max_length=100, examples=["Robert C. Martin"])
    isbn: str = Field(
        ...,
        pattern=r"^(?:\d{10}|\d{13})$",
        description="ISBN-10 ou ISBN-13, chiffres uniquement",
        examples=["9780132350884"],
    )
    year: int = Field(..., ge=1000, le=2100, examples=[2008])
    pages: int = Field(..., gt=0, le=10000, examples=[464])
    genre: Optional[str] = Field(None, max_length=50, examples=["Informatique"])
    available: bool = True
 
 
class BookCreate(BookBase):
    """Corps de requête pour POST et PUT (remplacement complet)."""
 
 
class BookPatch(BaseModel):
    """Corps de requête pour PATCH : tous les champs sont optionnels."""
 
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, pattern=r"^(?:\d{10}|\d{13})$")
    year: Optional[int] = Field(None, ge=1000, le=2100)
    pages: Optional[int] = Field(None, gt=0, le=10000)
    genre: Optional[str] = Field(None, max_length=50)
    available: Optional[bool] = None
 
 
class Book(BookBase):
    """Livre tel que renvoyé par l'API."""
 
    model_config = ConfigDict(from_attributes=True)
 
    id: int
    created_at: datetime
    updated_at: datetime
 
 
class ErrorResponse(BaseModel):
    detail: str
 
 