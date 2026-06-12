from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


#
class BookCreate(BaseModel):

    #
    title: str = Field(..., min_length=1, max_length=255, description="Título do livro")
    author: str = Field(..., min_length=1, max_length=255, description="Nome do autor")
    published_date: date = Field(..., description="Data de publicação (YYYY-MM-DD)")
    summary: Optional[str] = Field(None, description="Resumo opcional do livro")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "O Senhor dos Anéis",
                "author": "J.R.R. Tolkien",
                "published_date": "1954-07-29",
                "summary": "Uma épica jornada pela Terra Média.",
            }
        }
    }


#
class BookResponse(BookCreate):

    #
    id: int = Field(..., description="ID único gerado automaticamente")

    #
    model_config = {"from_attributes": True}
