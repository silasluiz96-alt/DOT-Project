from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


# Formulário de entrada — define os campos obrigatórios para cadastrar um livro
class BookCreate(BaseModel):

    # Título do livro — obrigatório, entre 1 e 255 caracteres
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


#Formulário de saída — o que a API devolve após cadastro ou consulta, incluindo o ID gerado
class BookResponse(BookCreate):

    #ID gerado automaticamente pelo banco após o cadastro
    id: int = Field(..., description="ID único gerado automaticamente")

    #Permite converter o objeto do banco de dados diretamente para esse formato de resposta
    model_config = {"from_attributes": True}
