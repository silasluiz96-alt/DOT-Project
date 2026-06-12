from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = "evidencias_q2.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    rightMargin=0.8 * inch,
    leftMargin=0.8 * inch,
    topMargin=0.8 * inch,
    bottomMargin=0.8 * inch,
)

styles = getSampleStyleSheet()

AZUL = colors.HexColor("#1a3c6e")
AZUL_CLARO = colors.HexColor("#dce8f7")
CINZA = colors.HexColor("#f4f4f4")
VERDE = colors.HexColor("#1e6e3a")
VERDE_CLARO = colors.HexColor("#d4edda")
LARANJA = colors.HexColor("#7a3e00")
LARANJA_CLARO = colors.HexColor("#fff3cd")
CODIGO_BG = colors.HexColor("#1e1e1e")
CODIGO_FG = colors.HexColor("#d4d4d4")

titulo_style = ParagraphStyle(
    "titulo", fontSize=20, leading=26, textColor=colors.white,
    alignment=TA_CENTER, fontName="Helvetica-Bold",
)
subtitulo_style = ParagraphStyle(
    "subtitulo", fontSize=12, leading=16, textColor=colors.white,
    alignment=TA_CENTER, fontName="Helvetica",
)
secao_style = ParagraphStyle(
    "secao", fontSize=13, leading=18, textColor=colors.white,
    fontName="Helvetica-Bold", alignment=TA_LEFT,
)
corpo_style = ParagraphStyle(
    "corpo", fontSize=10, leading=14, textColor=colors.black,
    fontName="Helvetica", alignment=TA_JUSTIFY,
)
corpo_bold_style = ParagraphStyle(
    "corpo_bold", fontSize=10, leading=14, textColor=colors.black,
    fontName="Helvetica-Bold",
)
label_style = ParagraphStyle(
    "label", fontSize=9, leading=12, textColor=AZUL,
    fontName="Helvetica-Bold",
)
code_style = ParagraphStyle(
    "code", fontSize=8, leading=11, textColor=CODIGO_FG,
    fontName="Courier", backColor=CODIGO_BG,
    leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4,
)
destaque_style = ParagraphStyle(
    "destaque", fontSize=10, leading=14, textColor=LARANJA,
    fontName="Helvetica-Bold", alignment=TA_CENTER,
)
rodape_style = ParagraphStyle(
    "rodape", fontSize=8, leading=10, textColor=colors.grey,
    alignment=TA_CENTER,
)

def cabecalho_secao(texto):
    dados = [[Paragraph(texto, secao_style)]]
    t = Table(dados, colWidths=[6.9 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AZUL),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    return t

def caixa_info(label, valor):
    dados = [
        [Paragraph(label, label_style), Paragraph(valor, corpo_style)]
    ]
    t = Table(dados, colWidths=[1.6 * inch, 5.3 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), AZUL_CLARO),
        ("BACKGROUND", (1, 0), (1, 0), CINZA),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("LINEBEFORE", (1, 0), (1, 0), 0.5, colors.lightgrey),
    ]))
    return t

def caixa_destaque(texto, bg=VERDE_CLARO, fg=VERDE):
    st = ParagraphStyle("dest2", fontSize=10, leading=14, textColor=fg,
                        fontName="Helvetica-Bold", alignment=TA_CENTER)
    dados = [[Paragraph(texto, st)]]
    t = Table(dados, colWidths=[6.9 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 1, fg),
    ]))
    return t

def bloco_conversa(pergunta, resposta_paragrafos):
    story = []
    # Pergunta
    pq = ParagraphStyle("pq", fontSize=9, leading=13, textColor=colors.HexColor("#003366"),
                        fontName="Helvetica-Bold", leftIndent=10)
    dados_p = [[Paragraph(f"Voce: {pergunta}", pq)]]
    tp = Table(dados_p, colWidths=[6.9 * inch])
    tp.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#e8f0fb")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#aac4e8")),
    ]))
    story.append(tp)
    story.append(Spacer(1, 4))

    # Resposta
    rp = ParagraphStyle("rp", fontSize=9, leading=13, textColor=colors.HexColor("#1a3c1a"),
                        fontName="Helvetica", leftIndent=10, alignment=TA_JUSTIFY)
    for para in resposta_paragrafos:
        dados_r = [[Paragraph(f"Chatbot: {para}", rp)]]
        tr = Table(dados_r, colWidths=[6.9 * inch])
        tr.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f0fbf0")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#a8d5a8")),
        ]))
        story.append(tr)
        story.append(Spacer(1, 2))

    return story

def bloco_codigo(codigo):
    linhas = codigo.strip().split("\n")
    conteudo = "\n".join(linhas)
    dados = [[Paragraph(conteudo.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]]
    t = Table(dados, colWidths=[6.9 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODIGO_BG),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#555555")),
    ]))
    return t


story = []

# ─── CAPA ────────────────────────────────────────────────────────────────────
capa_dados = [[Paragraph("EVIDENCIAS — QUESTAO 2", titulo_style)],
              [Paragraph("Chatbot com IA Generativa | LangChain + GPT-4", subtitulo_style)],
              [Paragraph("Prova Tecnica — Dot Digital Group", subtitulo_style)],
              [Paragraph("Candidato: Silas Luiz Bom Fim | 2025", subtitulo_style)]]
capa_t = Table(capa_dados, colWidths=[6.9 * inch])
capa_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), AZUL),
    ("TOPPADDING", (0, 0), (-1, -1), 14),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ("LEFTPADDING", (0, 0), (-1, -1), 16),
    ("RIGHTPADDING", (0, 0), (-1, -1), 16),
]))
story.append(capa_t)
story.append(Spacer(1, 18))

# ─── SEÇÃO 1 — OBJETIVO ──────────────────────────────────────────────────────
story.append(cabecalho_secao("1. Objetivo da Questao"))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Desenvolver um chatbot baseado em IA Generativa utilizando <b>LangChain</b> e o modelo "
    "<b>GPT-4</b> da OpenAI. O chatbot deve manter historico de conversa entre as mensagens, "
    "responder perguntas sobre programacao Python em portugues brasileiro e demonstrar "
    "raciocinio avancado ao lidar com problemas complexos.",
    corpo_style))
story.append(Spacer(1, 8))
story.append(caixa_destaque(
    "DESTAQUE: Os testes locais foram realizados com problemas de Calculo Numerico — "
    "disciplina universitaria de alta complexidade — para demonstrar que o chatbot vai "
    "muito alem de respostas superficiais sobre Python.",
    bg=LARANJA_CLARO, fg=LARANJA))
story.append(Spacer(1, 16))

# ─── SEÇÃO 2 — STACK ─────────────────────────────────────────────────────────
story.append(cabecalho_secao("2. Tecnologias Utilizadas"))
story.append(Spacer(1, 8))

stack = [
    ["Linguagem", "Python 3.10+"],
    ["Framework de IA", "LangChain + langchain-openai"],
    ["Modelo de Linguagem", "GPT-4 (OpenAI)"],
    ["Gerenciamento de Segredos", "python-dotenv (.env local — nunca versionado)"],
    ["Historico de Conversa", "SystemMessage, HumanMessage, AIMessage (LangChain Core)"],
    ["Execucao", "Terminal interativo (python main.py)"],
]
t_stack = Table(
    [[Paragraph(k, label_style), Paragraph(v, corpo_style)] for k, v in stack],
    colWidths=[2.0 * inch, 4.9 * inch]
)
t_stack.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), AZUL_CLARO),
    ("BACKGROUND", (1, 0), (1, -1), CINZA),
    ("ROWBACKGROUNDS", (1, 0), (1, -1), [CINZA, colors.white]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
]))
story.append(t_stack)
story.append(Spacer(1, 16))

# ─── SEÇÃO 3 — ESTRUTURA ─────────────────────────────────────────────────────
story.append(cabecalho_secao("3. Estrutura do Codigo"))
story.append(Spacer(1, 8))

arquivos = [
    ["main.py", "Logica principal: conexao ao GPT-4, historico de mensagens, loop interativo"],
    ["requirements.txt", "Dependencias: langchain, langchain-openai, python-dotenv"],
    [".env (local)", "Chave OPENAI_API_KEY — nunca versionada, protegida pelo .gitignore"],
    [".env.example", "Modelo de configuracao com placeholder 'sua_chave_aqui'"],
    ["README.md", "Instrucoes de instalacao, configuracao e execucao do chatbot"],
]
t_arq = Table(
    [[Paragraph(k, label_style), Paragraph(v, corpo_style)] for k, v in arquivos],
    colWidths=[1.8 * inch, 5.1 * inch]
)
t_arq.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1), AZUL_CLARO),
    ("ROWBACKGROUNDS", (1, 0), (1, -1), [CINZA, colors.white]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
]))
story.append(t_arq)
story.append(Spacer(1, 16))

# ─── SEÇÃO 4 — CÓDIGO FONTE ──────────────────────────────────────────────────
story.append(cabecalho_secao("4. Codigo-Fonte Principal (main.py)"))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "O arquivo <b>main.py</b> concentra toda a logica do chatbot. "
    "Cada parte foi comentada de forma didatica para facilitar a compreensao:",
    corpo_style))
story.append(Spacer(1, 6))

codigo_main = """import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Carrega as variaveis de ambiente do arquivo .env
load_dotenv()

# Le a chave da API da OpenAI a partir do .env
api_key = os.getenv("OPENAI_API_KEY")

# Conecta ao modelo GPT-4 da OpenAI usando a chave carregada
llm = ChatOpenAI(model="gpt-4", api_key=api_key)

# Mensagem de sistema — define o papel e o comportamento do chatbot
system_message = SystemMessage(
    content=(
        "Voce e um assistente especialista em programacao Python. "
        "Responda sempre em portugues brasileiro, de forma clara e didatica, "
        "com exemplos de codigo quando necessario."
    )
)

# Historico da conversa — comeca apenas com a mensagem de sistema
historico = [system_message]


def chat(pergunta: str) -> str:
    # Adiciona a pergunta do usuario ao historico
    historico.append(HumanMessage(content=pergunta))

    # Envia todo o historico ao modelo e obtem a resposta
    resposta = llm.invoke(historico)

    # Adiciona a resposta do modelo ao historico para manter o contexto
    historico.append(AIMessage(content=resposta.content))

    return resposta.content


if __name__ == "__main__":
    print("=== Chatbot Python ===")
    print("Especialista em programacao Python.")
    print("Digite 'sair' para encerrar.\\n")

    while True:
        pergunta = input("Voce: ").strip()
        if not pergunta:
            continue
        if pergunta.lower() == "sair":
            print("Encerrando o chatbot. Ate logo!")
            break
        resposta = chat(pergunta)
        print(f"\\nChatbot: {resposta}\\n")"""

story.append(bloco_codigo(codigo_main))
story.append(Spacer(1, 16))

story.append(PageBreak())

# ─── SEÇÃO 5 — TESTES ────────────────────────────────────────────────────────
story.append(cabecalho_secao("5. Testes Locais — Calculo Numerico"))
story.append(Spacer(1, 8))
story.append(caixa_destaque(
    "Os testes foram realizados com 4 problemas reais de Calculo Numerico — "
    "disciplina avancada da graduacao em Engenharia/Ciencia da Computacao. "
    "Isso comprova que o chatbot e capaz de resolver desafios matematicos e computacionais complexos, "
    "nao apenas responder perguntas basicas sobre Python.",
    bg=LARANJA_CLARO, fg=LARANJA))
story.append(Spacer(1, 10))

story.append(Paragraph(
    "Ambiente de execucao registrado no terminal (Windows 11):",
    corpo_bold_style))
story.append(Spacer(1, 4))
story.append(bloco_codigo(
    "Microsoft Windows [versao 10.0.26200.8655]\n"
    "C:\\Users\\silas> cd C:\\Users\\silas\\OneDrive\\Desktop\\dot-backend-test\\q2_chatbot\n"
    "C:\\...\\q2_chatbot> python main.py\n"
    "=== Chatbot Python ===\n"
    "Especialista em programacao Python.\n"
    "Digite 'sair' para encerrar."
))
story.append(Spacer(1, 14))

# --- Teste 1 ---
story.append(Paragraph("Teste 1 — Analise de Sistemas Lineares (Algebra Linear)", corpo_bold_style))
story.append(Spacer(1, 5))
story.append(Paragraph(
    "Problema classico de Calculo Numerico: dado um sistema linear Ax = b, determinar "
    "se ele possui unica solucao, infinitas solucoes ou nenhuma solucao. "
    "O chatbot aplicou o Teorema de Rouche-Capelli usando <b>NumPy</b> e o conceito de "
    "<b>rank</b> (posto) de matrizes.",
    corpo_style))
story.append(Spacer(1, 5))
story.append(Paragraph("Pergunta enviada ao chatbot:", label_style))
story.append(bloco_codigo(
    "escreva um programa em python que faz uma analise de um sistema linear\n"
    "e determina o numero de solucoes"
))
story.append(Spacer(1, 5))
story.append(Paragraph("Codigo gerado pelo chatbot:", label_style))
story.append(bloco_codigo(
    "import numpy as np\n\n"
    "def numero_solucoes(A, b):\n"
    "    A = np.array(A)\n"
    "    b = np.array(b)\n"
    "    rank_A = np.linalg.matrix_rank(A)\n"
    "    Ab = np.concatenate((A, b), axis=1)\n"
    "    rank_Ab = np.linalg.matrix_rank(Ab)\n"
    "    n = len(A[0])\n"
    "    if rank_A == rank_Ab:\n"
    "        if rank_A == n:\n"
    "            return 'Sistema possui unica solucao'\n"
    "        else:\n"
    "            return 'Sistema possui infinitas solucoes'\n"
    "    else:\n"
    "        return 'Sistema nao possui solucao'\n\n"
    "A = [[2, 3], [4, 6]]\n"
    "b = [[6], [12]]\n"
    "print(numero_solucoes(A, b))"
))
story.append(Spacer(1, 5))
story.append(caixa_destaque(
    "Resultado: O chatbot implementou corretamente o Teorema de Rouche-Capelli, "
    "comparando o posto da matriz dos coeficientes com a matriz aumentada.",
    bg=VERDE_CLARO, fg=VERDE))
story.append(Spacer(1, 14))

# --- Teste 2 ---
story.append(Paragraph("Teste 2 — Metodo de Newton-Raphson (Calculo de Raizes)", corpo_bold_style))
story.append(Spacer(1, 5))
story.append(Paragraph(
    "O Metodo de Newton-Raphson e um dos algoritmos mais utilizados em Calculo Numerico "
    "para encontrar raizes de funcoes nao-lineares de forma iterativa. "
    "O chatbot utilizou a biblioteca <b>SymPy</b> para calcular a derivada simbolica da funcao "
    "e implementou o loop iterativo com criterio de parada por tolerancia (epsilon).",
    corpo_style))
story.append(Spacer(1, 5))
story.append(Paragraph("Pergunta enviada ao chatbot:", label_style))
story.append(bloco_codigo(
    "quero um programa em python para calcular cada um dos valores\n"
    "utilizando o metodo de Newton-Raphson"
))
story.append(Spacer(1, 5))
story.append(Paragraph("Codigo gerado pelo chatbot:", label_style))
story.append(bloco_codigo(
    "import sympy as sp\n\n"
    "x = sp.symbols('x')\n"
    "f = x**3 - x**2 + 2\n"
    "f_prime = sp.diff(f, x)\n\n"
    "def newton_raphson(f, f_prime, x0, epsilon=1e-10, max_iter=100):\n"
    "    x = x0\n"
    "    for _ in range(max_iter):\n"
    "        x_old = x\n"
    "        x = x - f.subs('x', x)/f_prime.subs('x', x)\n"
    "        if abs(x - x_old) < epsilon:\n"
    "            break\n"
    "    return x\n\n"
    "x0 = -20\n"
    "root = newton_raphson(f, f_prime, x0)\n"
    "print(f'Raiz encontrada: {root}')"
))
story.append(Spacer(1, 5))
story.append(caixa_destaque(
    "Resultado: O chatbot implementou Newton-Raphson com derivada simbolica (SymPy), "
    "criterio de convergencia e limite de iteracoes — solucao robusta e correta.",
    bg=VERDE_CLARO, fg=VERDE))
story.append(Spacer(1, 14))

story.append(PageBreak())

# --- Teste 3 ---
story.append(cabecalho_secao("5. Testes Locais — Calculo Numerico (continuacao)"))
story.append(Spacer(1, 10))
story.append(Paragraph("Teste 3 — Metodo de Gauss-Seidel com Criterio das Linhas", corpo_bold_style))
story.append(Spacer(1, 5))
story.append(Paragraph(
    "O Metodo de Gauss-Seidel e um algoritmo iterativo para solucao de sistemas lineares. "
    "Este teste foi o mais complexo ate entao: alem de implementar o metodo, o chatbot "
    "verificou o <b>Criterio das Linhas</b> (condicao suficiente de convergencia) antes "
    "de executar as iteracoes — comportamento esperado de uma implementacao profissional.",
    corpo_style))
story.append(Spacer(1, 5))
story.append(Paragraph("Pergunta enviada ao chatbot:", label_style))
story.append(bloco_codigo(
    "Agora eu quero um programa em python para resolver o sistema linear dado\n"
    "usando o metodo de Gauss-Seidel, verificando se o criterio das linhas\n"
    "e satisfeito antes de continuar o algoritimo"
))
story.append(Spacer(1, 5))
story.append(Paragraph("Codigo gerado pelo chatbot:", label_style))
story.append(bloco_codigo(
    "import numpy as np\n\n"
    "def verifica_criterio_linhas(A):\n"
    "    n = len(A)\n"
    "    for i in range(n):\n"
    "        soma = sum(abs(A[i, j]) for j in range(n) if i != j)\n"
    "        if abs(A[i, i]) <= soma:\n"
    "            return False\n"
    "    return True\n\n"
    "def gauss_seidel(A, b, x0, max_iter=100):\n"
    "    if not verifica_criterio_linhas(A):\n"
    "        print('O sistema nao satisfaz o criterio das linhas')\n"
    "        return\n"
    "    n = len(A)\n"
    "    x = x0.copy()\n"
    "    for it in range(max_iter):\n"
    "        x_new = x.copy()\n"
    "        for i in range(n):\n"
    "            s1 = sum(A[i, j] * x_new[j] for j in range(i))\n"
    "            s2 = sum(A[i, j] * x[j] for j in range(i + 1, n))\n"
    "            x_new[i] = (b[i] - s1 - s2) / A[i, i]\n"
    "        if np.allclose(x, x_new, rtol=1e-8):\n"
    "            break\n"
    "        x = x_new\n"
    "    return x\n\n"
    "A = np.array([[4.0, 1.0, 1.0], [2.0, 5.0, 1.0], [1.0, 1.0, 3.0]])\n"
    "b = np.array([1.0, 1.0, 1.0])\n"
    "x0 = np.zeros_like(b)\n"
    "x = gauss_seidel(A, b, x0)\n"
    "print(f'Solucao: {x}')"
))
story.append(Spacer(1, 5))
story.append(caixa_destaque(
    "Resultado: O chatbot implementou o Criterio das Linhas corretamente e aplicou "
    "Gauss-Seidel com criterio de parada np.allclose — implementacao de nivel academico.",
    bg=VERDE_CLARO, fg=VERDE))
story.append(Spacer(1, 14))

# --- Teste 4 ---
story.append(Paragraph("Teste 4 — Integracao Numerica pelo Metodo dos Trapezios", corpo_bold_style))
story.append(Spacer(1, 5))
story.append(Paragraph(
    "Ultimo teste: calculo da integral definida de x<super>2</super> * ln(x) de 1 a 2 "
    "usando a Regra dos Trapezios com 7 pontos. "
    "Este metodo divide a area sob a curva em trapezios e soma suas areas para aproximar "
    "a integral. O chatbot explicou o metodo, codificou a solucao com <b>NumPy</b> "
    "e alertou sobre a natureza aproximada do resultado.",
    corpo_style))
story.append(Spacer(1, 5))
story.append(Paragraph("Pergunta enviada ao chatbot:", label_style))
story.append(bloco_codigo(
    "Escreva um programa em Python para calcular a integral de x^2 * ln(x)\n"
    "de 1 a 2 usando o Metodo dos Trapezios com 7 pontos."
))
story.append(Spacer(1, 5))
story.append(Paragraph("Codigo gerado pelo chatbot:", label_style))
story.append(bloco_codigo(
    "import numpy as np\n\n"
    "def f(x):\n"
    "    return x**2 * np.log(x)\n\n"
    "def trapezoidal_rule(a, b, n, func):\n"
    "    h = (b - a) / (n - 1)\n"
    "    x_values = np.linspace(a, b, n)\n"
    "    sum_values = func(a) + func(b) + 2 * sum([func(x) for x in x_values[1:-1]])\n"
    "    return h / 2 * sum_values\n\n"
    "a, b, n = 1, 2, 7\n"
    "area = trapezoidal_rule(a, b, n, f)\n"
    "print('A integral de x^2 * ln(x) de 1 a 2 com 7 pontos e aprox {:.8f}'.format(area))"
))
story.append(Spacer(1, 5))
story.append(caixa_destaque(
    "Resultado: O chatbot implementou a Regra dos Trapezios corretamente com np.linspace, "
    "formula de soma e passo h — resultado preciso para a aproximacao com 7 pontos.",
    bg=VERDE_CLARO, fg=VERDE))
story.append(Spacer(1, 14))

# ─── SEÇÃO 6 — TESTES NO CODESPACE ──────────────────────────────────────────
story.append(PageBreak())
story.append(cabecalho_secao("6. Testes via GitHub Codespaces"))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Alem dos testes locais via CMD, o chatbot foi executado diretamente pelo navegador "
    "usando o <b>GitHub Codespaces</b> — ambiente VS Code na nuvem integrado ao repositorio. "
    "Esta etapa comprova que o chatbot funciona em qualquer ambiente, sem depender de "
    "instalacao local.",
    corpo_style))
story.append(Spacer(1, 8))
story.append(caixa_destaque(
    "Ambiente: GitHub Codespaces (literate lamp) | Repositorio: silasluiz96-alt/DOT-Project | "
    "Branch: main | Sistema: Linux (Ubuntu) no navegador",
    bg=AZUL_CLARO, fg=AZUL))
story.append(Spacer(1, 10))

story.append(Paragraph("Teste 5 — Conceitos Basicos de Python para Iniciantes", corpo_bold_style))
story.append(Spacer(1, 5))
story.append(Paragraph(
    "Neste teste foi avaliada a capacidade do chatbot de orientar um aluno iniciante, "
    "listando os principais conceitos de Python com exemplos de codigo para cada topico. "
    "O chatbot estruturou uma resposta didatica cobrindo 7 conceitos fundamentais.",
    corpo_style))
story.append(Spacer(1, 5))
story.append(Paragraph("Pergunta enviada ao chatbot:", label_style))
story.append(bloco_codigo(
    "Sou um aluno aprendendo Python, quais os principais conceitos que devo ver primeiro?"
))
story.append(Spacer(1, 5))
story.append(Paragraph("Resumo da resposta gerada:", label_style))
story.append(bloco_codigo(
    "1. Sintaxe Basica — variaveis, funcoes, operadores\n"
    "   nome = 'Joao'\n"
    "   print('Ola, ' + nome)\n\n"
    "2. Tipos de Dados — int, float, str, list, tuple, dict\n"
    "   numero = 10 | decimal = 10.5 | lista = [1,2,3]\n\n"
    "3. Estruturas de Controle — if, else, for, while\n"
    "   if idade >= 18: print('Maior de idade')\n\n"
    "4. Funcoes — def, parametros, return\n"
    "   def somar(a, b): return a + b\n\n"
    "5. Classes e Objetos — POO, heranca, polimorfismo\n"
    "   class Pessoa: def __init__(self, nome, idade): ...\n\n"
    "6. Excecoes — try, except, tratamento de erros\n"
    "   try: x = 10/0 except ZeroDivisionError: print('Erro!')\n\n"
    "7. Manipulacao de Arquivos — open, read, write, close\n"
    "   arquivo = open('arquivo.txt', 'w')"
))
story.append(Spacer(1, 5))
story.append(caixa_destaque(
    "Resultado: O chatbot respondeu de forma estruturada e didatica, "
    "cobrindo 7 conceitos essenciais com exemplos de codigo para cada um.",
    bg=VERDE_CLARO, fg=VERDE))
story.append(Spacer(1, 14))

story.append(Paragraph("Teste 6 — Python para Calculo Numerico e Series de Taylor", corpo_bold_style))
story.append(Spacer(1, 5))
story.append(Paragraph(
    "Neste teste foi verificado se o chatbot consegue conectar o aprendizado de Python "
    "com aplicacoes matematicas avancadas. A pergunta abordou Calculo Numerico e Series de Taylor, "
    "demonstrando continuidade tematica com os testes anteriores realizados via CMD.",
    corpo_style))
story.append(Spacer(1, 5))
story.append(Paragraph("Pergunta enviada ao chatbot:", label_style))
story.append(bloco_codigo(
    "posso usar python para aprender calculo numerico?\n"
    "E equacoes como series de Taylor?"
))
story.append(Spacer(1, 5))
story.append(Paragraph("Codigo gerado pelo chatbot:", label_style))
story.append(bloco_codigo(
    "import math\n\n"
    "def calculate_taylor_approximation(x, n):\n"
    "    result = 0\n"
    "    for i in range(n):\n"
    "        coeff = (-1) ** i\n"
    "        num = x ** (2 * i + 1)\n"
    "        denom = math.factorial(2 * i + 1)\n"
    "        result += (coeff) * (num / denom)\n"
    "    return result\n\n"
    "x = 1.0\n"
    "print(calculate_taylor_approximation(x, 10))  # Aprox. de sin(1.0)"
))
story.append(Spacer(1, 5))
story.append(Paragraph(
    "O chatbot explicou que Python e ideal para Calculo Numerico graças as bibliotecas "
    "<b>NumPy</b>, <b>SciPy</b> e <b>matplotlib</b>, e implementou a aproximacao de "
    "sin(x) usando os primeiros n termos da Serie de Taylor — tecnica classica de "
    "Analise Numerica ensinada em cursos de Engenharia e Matematica.",
    corpo_style))
story.append(Spacer(1, 5))
story.append(caixa_destaque(
    "Resultado: O chatbot demonstrou dominio de Series de Taylor e sua implementacao "
    "numerica em Python — confirmando capacidade avancada de raciocinio matematico.",
    bg=VERDE_CLARO, fg=VERDE))
story.append(Spacer(1, 14))

# ─── SEÇÃO 7 — ENCERRAMENTO ───────────────────────────────────────────────────
story.append(cabecalho_secao("7. Encerramento da Sessao e Conclusao"))
story.append(Spacer(1, 8))
story.append(bloco_codigo(
    "# Sessao CMD (Windows 11)\n"
    "Voce: sair\n"
    "Encerrando o chatbot. Ate logo!\n\n"
    "# Sessao Codespaces (navegador)\n"
    "@silasluiz96-alt -> /workspaces/DOT-Project/q2_chatbot (main) $ python main.py\n"
    "=== Chatbot Python ===\n"
    "..."
))
story.append(Spacer(1, 10))

resumo = [
    ["Criterio", "Status"],
    ["Chatbot funcional com LangChain + GPT-4", "APROVADO"],
    ["Historico de conversa entre mensagens", "APROVADO"],
    ["Respostas em portugues brasileiro", "APROVADO"],
    ["Segredo (API Key) protegido via .env", "APROVADO"],
    ["4 testes via CMD com Calculo Numerico avancado", "APROVADO"],
    ["2 testes via GitHub Codespaces (navegador)", "APROVADO"],
    ["Codigo explicado e didatico", "APROVADO"],
    ["README com instrucoes completas", "APROVADO"],
]
t_res = Table(
    [[Paragraph(r[0], corpo_bold_style if i == 0 else corpo_style),
      Paragraph(r[1], ParagraphStyle("ok", fontSize=10, fontName="Helvetica-Bold",
                                      textColor=VERDE if i > 0 else colors.white,
                                      alignment=TA_CENTER))]
     for i, r in enumerate(resumo)],
    colWidths=[5.5 * inch, 1.4 * inch]
)
t_res.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), AZUL),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CINZA, colors.white]),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
]))
story.append(t_res)
story.append(Spacer(1, 12))
story.append(caixa_destaque(
    "Todos os criterios da Questao 2 foram atendidos com sucesso. "
    "Os testes com Calculo Numerico demonstram que o chatbot possui capacidade real "
    "de raciocinio e geracao de codigo Python avancado.",
    bg=VERDE_CLARO, fg=VERDE))
story.append(Spacer(1, 16))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Documento gerado automaticamente como evidencia da Questao 2 — "
    "Prova Tecnica Dot Digital Group | Candidato: Silas Luiz Bom Fim | 2025",
    rodape_style))

doc.build(story)
print(f"PDF gerado com sucesso: {OUTPUT}")
