# Q2 — Chatbot com IA Generativa

Chatbot especialista em programação Python, desenvolvido com **LangChain** e **GPT-4** da OpenAI.

## Como rodar

### 1. Instale as dependências
```bash
cd q2_chatbot
pip install -r requirements.txt
```

### 2. Configure a chave da API
```bash
cp .env.example .env
```
Abra o arquivo `.env` e substitua `sua_chave_aqui` pela sua chave da OpenAI.

### 3. Execute o chatbot
```bash
python main.py
```

## Exemplo de uso

```
=== Chatbot Python ===
Especialista em programação Python.
Digite 'sair' para encerrar.

Você: Como criar uma lista em Python?

Chatbot: Em Python, você pode criar uma lista usando colchetes []...

Você: sair
Encerrando o chatbot. Até logo!
```

## Funcionalidades

- Responde perguntas sobre programação em Python
- Mantém histórico da conversa durante a sessão
- Respostas em português brasileiro com exemplos de código
- Encerra ao digitar `sair`

## Requisitos

- Python 3.10+
- Chave de API da OpenAI (GPT-4)
