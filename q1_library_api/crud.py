from typing import Optional
from sqlalchemy.orm import Session
import models
import schemas


#
def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    #
    novo_livro = models.Book(
        title=book.title,
        author=book.author,
        published_date=book.published_date,
        summary=book.summary,
    )
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


#
def get_books(
    db: Session,
    title: Optional[str] = None,
    author: Optional[str] = None,
) -> list[models.Book]:
    #
    query = db.query(models.Book)

    if title:
        #
        query = query.filter(models.Book.title.ilike(f"%{title}%"))

    if author:
        #
        query = query.filter(models.Book.author.ilike(f"%{author}%"))

    return query.all()


#
def get_book_by_id(db: Session, book_id: int) -> Optional[models.Book]:
    #
    return db.query(models.Book).filter(models.Book.id == book_id).first()
