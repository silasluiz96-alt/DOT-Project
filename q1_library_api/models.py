from sqlalchemy import Column, Integer, String, Date, Text
from database import Base


#Esse vai representar a tabela de livros no banco de dados
class Book(Base):

    #Nome da tabela que será criada no banco de dados
    __tablename__ = "books"

    #Identificador único de cada livro, gerado automaticamente pelo banco
    id = Column(Integer, primary_key=True, index=True)

    #Título do Livro
    title = Column(String(255), nullable=False, index=True)

    #Nome do Autor
    author = Column(String(255), nullable=False, index=True)

    #Data de Publicação
    published_date = Column(Date, nullable=False)

    #Resumo do livro em texto livre — opcional. Será usado somente se o usuário quiser comentar
    summary = Column(Text, nullable=True)
