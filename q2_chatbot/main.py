import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Lê a chave da API da OpenAI a partir do .env
api_key = os.getenv("OPENAI_API_KEY")

# Conecta ao modelo GPT-4 da OpenAI usando a chave carregada
llm = ChatOpenAI(model="gpt-4", api_key=api_key)

# Mensagem de sistema — define o papel e o comportamento do chatbot
system_message = SystemMessage(
    content=(
        "Você é um assistente especialista em programação Python. "
        "Responda sempre em português brasileiro, de forma clara e didática, "
        "com exemplos de código quando necessário."
    )
)

# Histórico da conversa — começa apenas com a mensagem de sistema
historico = [system_message]


def chat(pergunta: str) -> str:
    # Adiciona a pergunta do usuário ao histórico
    historico.append(HumanMessage(content=pergunta))

    # Envia todo o histórico ao modelo e obtém a resposta
    resposta = llm.invoke(historico)

    # Adiciona a resposta do modelo ao histórico para manter o contexto
    historico.append(AIMessage(content=resposta.content))

    return resposta.content


# Ponto de entrada do programa
if __name__ == "__main__":
    print("=== Chatbot Python ===")
    print("Especialista em programação Python.")
    print("Digite 'sair' para encerrar.\n")

    # Loop principal — continua até o usuário digitar 'sair'
    while True:
        pergunta = input("Você: ").strip()

        if not pergunta:
            continue

        if pergunta.lower() == "sair":
            print("Encerrando o chatbot. Até logo!")
            break

        # Envia a pergunta e exibe a resposta
        resposta = chat(pergunta)
        print(f"\nChatbot: {resposta}\n")
