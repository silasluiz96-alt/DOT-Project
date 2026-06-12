from typing import Optional
from sqlalchemy.orm import Session
import models
import schemas


# Função responsável por cadastrar um novo livro no banco de dados
def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    # Cria o objeto livro com os dados recebidos do usuário
    novo_livro = models.Book(
        title=book.title,
        author=book.author,
        published_date=book.published_date,
        summary=book.summary,
    )
    # Salva o livro no banco, confirma a transação e atualiza o objeto com o ID gerado
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


# Função responsável por listar livros, com filtro opcional por título ou autor
def get_books(
    db: Session,
    title: Optional[str] = None,
    author: Optional[str] = None,
) -> list[models.Book]:
    # Inicia a consulta buscando todos os livros
    query = db.query(models.Book)

    if title:
        # Filtra pelo título — busca parcial e sem diferenciar maiúsculas
        query = query.filter(models.Book.title.ilike(f"%{title}%"))

    if author:
        # Filtra pelo autor — busca parcial e sem diferenciar maiúsculas
        query = query.filter(models.Book.author.ilike(f"%{author}%"))

    return query.all()


# Função responsável por buscar um livro específico pelo seu ID
def get_book_by_id(db: Session, book_id: int) -> Optional[models.Book]:
    # Retorna o primeiro livro encontrado com esse ID, ou None se não existir
    return db.query(models.Book).filter(models.Book.id == book_id).first()
