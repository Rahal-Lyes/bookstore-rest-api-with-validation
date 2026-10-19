 
from fastapi import FastAPI

from app.routers import books

app = FastAPI(
    title="Books API",
    description="API RESTful pour gérer une bibliothèque de livres (CRUD, "
    "validation Pydantic, filtrage et pagination).",
    version="1.0.0",
)
app.include_router(books.router)


@app.get("/", tags=["Santé"])
def root():
    return {"message": "API opérationnelle"}