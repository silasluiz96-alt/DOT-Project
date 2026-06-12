"""
Corpus de documentos academicos para busca semantica.
Textos extraidos de 5 artigos cientificos reais via pdfplumber.
"""

import logging
import pdfplumber
import fitz  # pymupdf — melhor para PDFs com layout de duas colunas
import re
import os

# Suprimir avisos de PDF com CropBox faltando (cosmético, não afeta a leitura)
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Caminhos dos PDFs (relativos ao diretorio do projeto)
_BASE = os.path.dirname(os.path.abspath(__file__))

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
    """Usa pymupdf para PDFs com layout de multiplas colunas — preserva espacos corretamente."""
    doc = fitz.open(caminho_pdf)
    paginas = []
    for i in range(min(max_paginas, len(doc))):
        t = doc[i].get_text()
        if t and t.strip():
            paginas.append(t.strip())
    return "\n\n".join(paginas)


def _extrair_texto(caminho_pdf: str, max_paginas: int = 10) -> str:
    """Le um PDF pagina por pagina e retorna o texto completo."""
    with pdfplumber.open(caminho_pdf) as pdf:
        paginas = []
        for page in pdf.pages[:max_paginas]:
            t = page.extract_text()
            if t:
                paginas.append(t.strip())
    return "\n\n".join(paginas)


def _dividir_em_paragrafos(texto: str, min_chars: int = 200, max_chars: int = 1200) -> list[str]:
    """
    Divide o texto em paragrafos naturais (quebras de linha dupla).
    Paragrafos muito curtos sao unidos ao seguinte.
    Paragrafos muito longos sao divididos no meio de forma limpa.
    """
    # Separar por linha dupla (fim de paragrafo natural no PDF)
    blocos = re.split(r"\n{2,}", texto)

    paragrafos = []
    buffer = ""

    for bloco in blocos:
        bloco = re.sub(r"\s+", " ", bloco).strip()
        if not bloco:
            continue

        buffer = (buffer + " " + bloco).strip() if buffer else bloco

        if len(buffer) >= min_chars:
            # Se ficou grande demais, divide sem cortar palavras
            while len(buffer) > max_chars:
                corte = buffer.rfind(" ", 0, max_chars)
                if corte == -1:
                    corte = max_chars
                paragrafos.append(buffer[:corte].strip())
                buffer = buffer[corte:].strip()
            paragrafos.append(buffer)
            buffer = ""

    if buffer and len(buffer) >= min_chars:
        paragrafos.append(buffer)

    return paragrafos


def carregar_documentos() -> tuple[list[str], list[dict]]:
    """
    Carrega todos os PDFs, divide em paragrafos e retorna:
    - lista de textos (um por paragrafo)
    - lista de metadados (titulo, autores, publicacao de cada paragrafo)
    """
    textos = []
    metadados = []

    for chave, info in FONTES.items():
        print(f"  Carregando: {info['titulo'][:60]}...")
        # PDFs em ingles com layout multi-coluna — pymupdf preserva espacos e acentos corretamente
        if chave in ("digital_transformation", "machine_failure"):
            texto = _extrair_com_pymupdf(info["arquivo"])
        else:
            texto = _extrair_texto(info["arquivo"])
        paragrafos = _dividir_em_paragrafos(texto)

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
