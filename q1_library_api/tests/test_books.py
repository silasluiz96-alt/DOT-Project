import sys
import os

#
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

#
TEST_DATABASE_URL = "sqlite:///./test_library.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    #
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


#
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    #
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


#
client = TestClient(app)

#
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
    #
    resposta = client.post("/books/", json=LIVRO_VALIDO)
    assert resposta.status_code == 201
    dados = resposta.json()
    assert dados["title"] == LIVRO_VALIDO["title"]
    assert dados["author"] == LIVRO_VALIDO["author"]
    assert "id" in dados


def test_cadastrar_livro_sem_titulo():
    #
    livro = {k: v for k, v in LIVRO_VALIDO.items() if k != "title"}
    resposta = client.post("/books/", json=livro)
    assert resposta.status_code == 422


def test_cadastrar_livro_sem_autor():
    #
    livro = {k: v for k, v in LIVRO_VALIDO.items() if k != "author"}
    resposta = client.post("/books/", json=livro)
    assert resposta.status_code == 422


def test_cadastrar_livro_data_invalida():
    #
    livro = {**LIVRO_VALIDO, "published_date": "29/07/1954"}
    resposta = client.post("/books/", json=livro)
    assert resposta.status_code == 422


def test_cadastrar_livro_sem_resumo():
    #
    livro = {k: v for k, v in LIVRO_VALIDO.items() if k != "summary"}
    resposta = client.post("/books/", json=livro)
    assert resposta.status_code == 201
    assert resposta.json()["summary"] is None


# --- GET /books ---

def test_listar_livros_vazio():
    #
    resposta = client.get("/books/")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_listar_todos_os_livros():
    #
    client.post("/books/", json=LIVRO_VALIDO)
    client.post("/books/", json=LIVRO_2)
    resposta = client.get("/books/")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_filtrar_por_titulo():
    #
    client.post("/books/", json=LIVRO_VALIDO)
    client.post("/books/", json=LIVRO_2)
    resposta = client.get("/books/?title=Dom Casmurro")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["title"] == "Dom Casmurro"


def test_filtrar_por_autor():
    #
    client.post("/books/", json=LIVRO_VALIDO)
    client.post("/books/", json=LIVRO_2)
    resposta = client.get("/books/?author=Machado")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_filtrar_titulo_sem_resultado():
    #
    client.post("/books/", json=LIVRO_VALIDO)
    resposta = client.get("/books/?title=Harry Potter")
    assert resposta.status_code == 200
    assert resposta.json() == []


# --- GET /books/{id} ---

def test_buscar_livro_por_id_existente():
    #
    cadastro = client.post("/books/", json=LIVRO_VALIDO).json()
    resposta = client.get(f"/books/{cadastro['id']}")
    assert resposta.status_code == 200
    assert resposta.json()["id"] == cadastro["id"]


def test_buscar_livro_por_id_inexistente():
    #
    resposta = client.get("/books/9999")
    assert resposta.status_code == 404
    assert "não encontrado" in resposta.json()["detail"]


def test_endpoint_raiz():
    #
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "mensagem" in resposta.json()
