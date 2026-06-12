from fastapi import FastAPI
from database import Base, engine
from routers import books

#
Base.metadata.create_all(bind=engine)

#
app = FastAPI(
    title="Biblioteca Virtual API",
    description="API para cadastro e consulta de livros. Desenvolvida com FastAPI + SQLite.",
    version="1.0.0",
)

#
app.include_router(books.router)


#
@app.get("/", tags=["Raiz"])
def root():
    #
    return {"mensagem": "Bem-vindo à Biblioteca Virtual! Acesse /docs para ver a documentação."}
