# CLAUDE.md — dot-backend-test

## O que é este projeto
Monorepo de prova técnica para processo seletivo de Desenvolvedor Backend com foco em IA (Dot Digital Group).
Contém 3 questões independentes implementadas em Python.

## Acordo de Boas Práticas
Este projeto segue o /acordo de Silas Luiz Bom Fim.
Consulte a skill `/acordo` no início de cada sessão.

## Questões
| Pasta                  | Questão                        | Stack                              |
|------------------------|--------------------------------|------------------------------------|
| `q1_library_api/`      | API de Biblioteca Virtual      | FastAPI + SQLite + SQLAlchemy + pytest |
| `q2_chatbot/`          | Chatbot com IA Generativa      | LangChain + GPT-4 (OpenAI)         |
| `q3_semantic_search/`  | Busca Semântica com Embeddings | Sentence Transformers + FAISS      |

## Metodologia de trabalho
Humano → IA → Humano (double checking rigoroso)
- Nenhuma etapa avança sem validação do Agente Humano
- Todo código entra via Pull Request
- Commits técnicos + commits didáticos separados

## Regras de branch
```
main          ← protegido, nunca recebe push direto
  └── feat/*  ← novas funcionalidades
  └── fix/*   ← correções
  └── docs/*  ← comentários didáticos (preenchidos no merge)
```

## Secrets
- `.env` NUNCA é commitado (está no `.gitignore`)
- Use `.env.example` como modelo para configurar localmente

## Status
- [ ] Q1 — API de Biblioteca Virtual
- [ ] Q2 — Chatbot com IA Generativa
- [ ] Q3 — Busca Semântica com Embeddings
