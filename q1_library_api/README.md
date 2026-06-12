# Q1 — API de Biblioteca Virtual

API REST para gerenciamento de livros, desenvolvida com **FastAPI**, **SQLAlchemy** e banco de dados **SQLite**.

## Evidências

📄 [Documento de evidências — evidencias_q1.pdf](../docs/evidencias_q1.pdf)

## Como rodar

### 1. Instale as dependências
```bash
cd q1_library_api
pip install -r requirements.txt
```

### 2. Execute a API
```bash
uvicorn main:app --reload
```

### 3. Acesse a documentação interativa
```
http://localhost:8000/docs
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/books/` | Cadastra um novo livro |
| GET | `/books/` | Lista todos os livros (com filtros) |
| GET | `/books/{id}` | Busca um livro pelo ID |

## Testes

```bash
pytest tests/
```

13 testes automatizados cobrindo todos os endpoints.

## Requisitos

- Python 3.10+
- Sem necessidade de banco de dados externo (SQLite gerado automaticamente)
