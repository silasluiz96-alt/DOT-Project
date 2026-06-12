from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import crud
import schemas
from database import get_db

# Agrupa todos os endpoints relacionados a livros sob o prefixo /books
router = APIRouter(
    prefix="/books",
    tags=["Livros"],
)


# Endpoint para cadastrar um novo livro — recebe os dados e salva no banco
@router.post(
    "/",
    response_model=schemas.BookResponse,
    status_code=201,
    summary="Cadastrar livro",
    description="Cadastra um novo livro na biblioteca com título, autor, data de publicação e resumo.",
)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # Chama a função de cadastro e retorna o livro criado com o ID gerado
    return crud.create_book(db=db, book=book)


# Endpoint para listar todos os livros — aceita filtros opcionais por título ou autor
@router.get(
    "/",
    response_model=list[schemas.BookResponse],
    summary="Listar livros",
    description="Retorna todos os livros. Use ?title= ou ?author= para filtrar.",
)
def list_books(
    title: Optional[str] = Query(None, description="Filtrar por título (busca parcial)"),
    author: Optional[str] = Query(None, description="Filtrar por autor (busca parcial)"),
    db: Session = Depends(get_db),
):
    # Chama a função de listagem repassando os filtros informados pelo usuário
    return crud.get_books(db=db, title=title, author=author)


# Endpoint para buscar um livro específico pelo ID informado na URL
@router.get(
    "/{book_id}",
    response_model=schemas.BookResponse,
    summary="Buscar livro por ID",
    description="Retorna os dados de um livro específico pelo seu ID.",
)
def get_book(book_id: int, db: Session = Depends(get_db)):
    # Busca o livro no banco — se não encontrar, retorna erro 404 para o usuário
    livro = crud.get_book_by_id(db=db, book_id=book_id)
    if not livro:
        raise HTTPException(status_code=404, detail=f"Livro com ID {book_id} não encontrado.")
    return livro
