# dot-backend-test

Prova técnica para Desenvolvedor Backend com foco em IA — **Dot Digital Group**.

## Questões

| # | Pasta | Descrição | Stack |
|---|-------|-----------|-------|
| 1 | `q1_library_api/` | API de Biblioteca Virtual | FastAPI + SQLite + SQLAlchemy |
| 2 | `q2_chatbot/` | Chatbot com IA Generativa | LangChain + GPT-4 |
| 3 | `q3_semantic_search/` | Busca Semântica com Embeddings | Sentence Transformers + FAISS |

## Como rodar cada questão

### Q1 — API de Biblioteca
```bash
cd q1_library_api
pip install -r requirements.txt
uvicorn main:app --reload
# Documentação: http://localhost:8000/docs
```

### Q2 — Chatbot
```bash
cd q2_chatbot
pip install -r requirements.txt
cp .env.example .env   # preencha com sua OPENAI_API_KEY
python main.py
```

### Q3 — Busca Semântica
```bash
cd q3_semantic_search
pip install -r requirements.txt
python main.py
```

## Requisitos gerais
- Python 3.10+
- Cada questão possui seu próprio `requirements.txt`
- Secrets ficam em `.env` local — nunca commitado
