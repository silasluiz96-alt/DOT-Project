import sys
import os

# Garante que o Python encontre os módulos da aplicação durante os testes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

# Banco de dados separado usado apenas durante os testes — não afeta o banco real
TEST_DATABASE_URL = "sqlite:///./test_library.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    # Substitui o banco real pelo banco de testes durante a execução
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Redireciona a aplicação para usar o banco de testes em vez do banco real
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    # Cria as tabelas antes de cada teste e apaga tudo ao final — banco sempre limpo
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# Cliente que simula requisições HTTP sem precisar de um servidor rodando
client = TestClient(app)

# Dados de exemplo reutilizados nos testes
LIVRO_VALIDO = {
    "title": "Dom Casmurro",
    "author": "Machado de Assis",
    "published_date": "1899-01-01",
    "summary": "Um clássico da literatura brasileira.",
}

LIVRO_2 = {
    "title": "Memórias Póstumas de Brás Cubas",
    "author": "Machado de Assis",
    "published_date": "1881-01-01",
    "summary": "Narrado por um defunto autor.",
}


# --- POST /books ---

def test_cadastrar_livro_sucesso():
    # Deve cadastrar com sucesso e retornar status 201 com ID gerado
    resposta = client.post("/books/", json=LIVRO_VALIDO)
    assert resposta.status_code == 201
    dados = resposta.json()
    assert dados["title"] == LIVRO_VALIDO["title"]
    assert dados["author"] == LIVRO_VALIDO["author"]
    assert "id" in dados


def test_cadastrar_livro_sem_titulo():
    #Deve rejeitar cadastro sem título e retornar erro de validação 422
    livro = {k: v for k, v in LIVRO_VALIDO.items() if k != "title"}
    resposta = client.post("/books/", json=livro)
    assert resposta.status_code == 422


def test_cadastrar_livro_sem_autor():
    # Deve rejeitar cadastro sem autor e retornar erro de validação 422
    livro = {k: v for k, v in LIVRO_VALIDO.items() if k != "author"}
    resposta = client.post("/books/", json=livro)
    assert resposta.status_code == 422


def test_cadastrar_livro_data_invalida():
    # Deve rejeitar data em formato inválido e retornar erro de validação 422
    livro = {**LIVRO_VALIDO, "published_date": "29/07/1954"}
    resposta = client.post("/books/", json=livro)
    assert resposta.status_code == 422


def test_cadastrar_livro_sem_resumo():
    # Resumo é opcional — deve aceitar o cadastro e retornar summary como nulo
    livro = {k: v for k, v in LIVRO_VALIDO.items() if k != "summary"}
    resposta = client.post("/books/", json=livro)
    assert resposta.status_code == 201
    assert resposta.json()["summary"] is None


# --- GET /books ---

def test_listar_livros_vazio():
    # Deve retornar lista vazia quando não há livros cadastrados
    resposta = client.get("/books/")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_listar_todos_os_livros():
    # Deve retornar todos os livros cadastrados
    client.post("/books/", json=LIVRO_VALIDO)
    client.post("/books/", json=LIVRO_2)
    resposta = client.get("/books/")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_filtrar_por_titulo():
    # Deve retornar apenas o livro cujo título bate com o filtro
    client.post("/books/", json=LIVRO_VALIDO)
    client.post("/books/", json=LIVRO_2)
    resposta = client.get("/books/?title=Dom Casmurro")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["title"] == "Dom Casmurro"


def test_filtrar_por_autor():
    # Deve retornar todos os livros do autor informado
    client.post("/books/", json=LIVRO_VALIDO)
    client.post("/books/", json=LIVRO_2)
    resposta = client.get("/books/?author=Machado")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_filtrar_titulo_sem_resultado():
    # Deve retornar lista vazia quando nenhum livro bate com o filtro
    client.post("/books/", json=LIVRO_VALIDO)
    resposta = client.get("/books/?title=Harry Potter")
    assert resposta.status_code == 200
    assert resposta.json() == []


# --- GET /books/{id} ---

def test_buscar_livro_por_id_existente():
    # Deve retornar o livro correto quando o ID existe
    cadastro = client.post("/books/", json=LIVRO_VALIDO).json()
    resposta = client.get(f"/books/{cadastro['id']}")
    assert resposta.status_code == 200
    assert resposta.json()["id"] == cadastro["id"]


def test_buscar_livro_por_id_inexistente():
    # Deve retornar erro 404 quando o ID não existe
    resposta = client.get("/books/9999")
    assert resposta.status_code == 404
    assert "não encontrado" in resposta.json()["detail"]


def test_endpoint_raiz():
    # Deve retornar mensagem de boas-vindas na raiz da API
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "mensagem" in resposta.json()
