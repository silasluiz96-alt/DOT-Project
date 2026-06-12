"""
Corpus de documentos academicos para busca semantica.
Textos extraidos de 5 artigos cientificos reais via pdfplumber e PyMuPDF.

Este arquivo e responsavel por duas tarefas:
  1. Ler os PDFs e extrair o texto de cada pagina
  2. Dividir o texto em paragrafos para que a busca seja mais precisa
"""

import logging
import pdfplumber          # le PDFs de coluna unica (artigos em portugues)
import fitz                # PyMuPDF — le PDFs com layout de multiplas colunas (artigos em ingles)
import re
import os

# Silencia avisos internos do pdfplumber sobre PDFs sem CropBox
# (problema cosmético do arquivo, nao afeta a leitura)
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Caminho base: pasta onde este arquivo esta salvo
_BASE = os.path.dirname(os.path.abspath(__file__))

# Mapa de todos os artigos do corpus com seus metadados
# Cada artigo virou um "documento" que o sistema vai aprender a buscar
FONTES = {
    "inovacao_aberta": {
        "titulo": "Inovacao aberta nas estrategias competitivas das empresas brasileiras",
        "autores": "Claudio Pitassi",
        "publicacao": "REBRAE, 2014",
        "arquivo": os.path.join(_BASE, "pdfs", "inovacao_aberta.pdf"),
    },
    "ia_relacoes_trabalho": {
        "titulo": "Inteligencia Artificial e Inovacao Tecnologica: Impactos nas Relacoes de Trabalho",
        "autores": "Claudio Teixeira Damilano",
        "publicacao": "Congresso Internacional, UFSM, 2019",
        "arquivo": os.path.join(_BASE, "pdfs", "ia_relacoes_trabalho.pdf"),
    },
    "ia_generativa_mercado": {
        "titulo": "Adocao de Inovacao de IA Generativa em Inteligencia e Pesquisa de Mercado",
        "autores": "Daniel Dias Madeira, Diego dos Santos Vega Senise",
        "publicacao": "ABRAPCORP / USP, 2025",
        "arquivo": os.path.join(_BASE, "pdfs", "ia_generativa_mercado.pdf"),
    },
    "digital_transformation": {
        "titulo": "Understanding digital transformation: A review and a research agenda",
        "autores": "Gregory Vial",
        "publicacao": "Journal of Strategic Information Systems, 2019",
        "arquivo": os.path.join(_BASE, "pdfs", "digital_transformation.pdf"),
    },
    "machine_failure": {
        "titulo": "Integration of Data Analytics and Data Mining for Machine Failure Mitigation",
        "autores": "Silas Luiz Bomfim et al.",
        "publicacao": "Logistics / MDPI, 2025",
        "arquivo": os.path.join(_BASE, "pdfs", "machine_failure.pdf"),
    },
}


def _extrair_com_pymupdf(caminho_pdf: str, max_paginas: int = 10) -> str:
    """
    Extrai texto usando PyMuPDF (biblioteca fitz).

    Usado para PDFs com layout de duas colunas (artigos academicos internacionais),
    onde o pdfplumber juntaria palavras de colunas diferentes sem espaco entre elas.
    O PyMuPDF le cada coluna separadamente e preserva os espacos corretamente.
    """
    doc = fitz.open(caminho_pdf)
    paginas = []
    for i in range(min(max_paginas, len(doc))):
        t = doc[i].get_text()
        if t and t.strip():
            paginas.append(t.strip())
    # Cada pagina e separada por linha dupla para o chunking reconhece-las
    return "\n\n".join(paginas)


def _extrair_texto(caminho_pdf: str, max_paginas: int = 10) -> str:
    """
    Extrai texto usando pdfplumber.

    Usado para PDFs de coluna unica (artigos em portugues).
    Cada pagina e lida individualmente e unida com separador de paragrafo.
    """
    with pdfplumber.open(caminho_pdf) as pdf:
        paginas = []
        for page in pdf.pages[:max_paginas]:
            t = page.extract_text()
            if t:
                paginas.append(t.strip())
    return "\n\n".join(paginas)


def _dividir_em_paragrafos(texto: str, min_chars: int = 200, max_chars: int = 1200) -> list[str]:
    """
    Divide o texto em paragrafos naturais para melhorar a qualidade da busca.

    Por que dividir em paragrafos e nao em pedacos fixos de caracteres?
    Porque um paragrafo tem uma ideia completa — o modelo de embedding consegue
    entender melhor o significado de um paragrafo do que de um pedaco cortado no meio.

    Regras aplicadas:
      - Paragrafos muito curtos (< min_chars) sao unidos ao seguinte
      - Paragrafos muito longos (> max_chars) sao cortados sem quebrar palavras
      - Pedacos menores que min_chars sao descartados (geralmente cabecalhos ou rodapes)
    """
    # Separar o texto nas quebras duplas de linha (fim de paragrafo natural)
    blocos = re.split(r"\n{2,}", texto)

    paragrafos = []
    buffer = ""  # acumula blocos curtos ate atingir o tamanho minimo

    for bloco in blocos:
        # Normalizar espacos internos do bloco
        bloco = re.sub(r"\s+", " ", bloco).strip()
        if not bloco:
            continue

        # Adicionar bloco ao buffer
        buffer = (buffer + " " + bloco).strip() if buffer else bloco

        if len(buffer) >= min_chars:
            # Se passou do tamanho maximo, cortar sem quebrar palavras
            while len(buffer) > max_chars:
                corte = buffer.rfind(" ", 0, max_chars)
                if corte == -1:
                    corte = max_chars
                paragrafos.append(buffer[:corte].strip())
                buffer = buffer[corte:].strip()
            paragrafos.append(buffer)
            buffer = ""

    # Salvar o que sobrou no buffer (ultimo paragrafo do documento)
    if buffer and len(buffer) >= min_chars:
        paragrafos.append(buffer)

    return paragrafos


def carregar_documentos() -> tuple[list[str], list[dict]]:
    """
    Funcao principal deste arquivo.

    Le todos os PDFs do corpus, divide em paragrafos e retorna duas listas paralelas:
      - textos: cada elemento e um paragrafo de um artigo
      - metadados: cada elemento e um dicionario com titulo, autores e publicacao

    As duas listas tem o mesmo tamanho — o indice i em textos corresponde
    ao mesmo indice i em metadados. Isso permite saber de qual artigo
    veio cada paragrafo retornado pela busca.
    """
    textos = []
    metadados = []

    for chave, info in FONTES.items():
        print(f"  Carregando: {info['titulo'][:60]}...")

        # PDFs em ingles com layout de multiplas colunas precisam do PyMuPDF
        # para preservar os espacos entre palavras corretamente
        if chave in ("digital_transformation", "machine_failure"):
            texto = _extrair_com_pymupdf(info["arquivo"])
        else:
            texto = _extrair_texto(info["arquivo"])

        paragrafos = _dividir_em_paragrafos(texto)

        # Cada paragrafo recebe uma copia dos metadados do seu artigo de origem
        for paragrafo in paragrafos:
            textos.append(paragrafo)
            metadados.append({
                "id": chave,
                "titulo": info["titulo"],
                "autores": info["autores"],
                "publicacao": info["publicacao"],
            })

    print(f"  Total: {len(textos)} trechos carregados de {len(FONTES)} artigos.\n")
    return textos, metadados
