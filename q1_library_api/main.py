from fastapi import FastAPI
from database import Base, engine
from routers import books

# Cria todas as tabelas no banco de dados SQLite ao iniciar a aplicação
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação FastAPI com título, descrição e versão
app = FastAPI(
    title="Biblioteca Virtual API",
    description="API para cadastro e consulta de livros. Desenvolvida com FastAPI + SQLite.",
    version="1.0.0",
)

# Registra as rotas de livros no aplicativo principal
app.include_router(books.router)


# Rota raiz — retorna uma mensagem de boas-vindas
@app.get("/", tags=["Raiz"])
def root():
    # Direciona o usuário para a documentação interativa em /docs
    return {"mensagem": "Bem-vindo à Biblioteca Virtual! Acesse /docs para ver a documentação."}
