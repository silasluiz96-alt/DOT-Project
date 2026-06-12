"""
Q3 — Busca Semantica com Embeddings e FAISS

O que este programa faz (em linguagem simples):
  Imagine que cada trecho de texto vira um ponto num mapa gigante.
  Textos com significado parecido ficam proximos nesse mapa.
  Quando voce faz uma pergunta, ela tambem vira um ponto —
  e o sistema encontra os pontos mais proximos a ela.

Fluxo do programa:
  1. Le os PDFs e divide em paragrafos (documents.py)
  2. Converte cada paragrafo em um vetor de numeros (embedding)
  3. Guarda todos os vetores no FAISS (vector store)
  4. Aguarda a pergunta do usuario
  5. Converte a pergunta em vetor e busca os mais proximos
  6. Se a pergunta for em portugues e o trecho em ingles, traduz automaticamente

Stack:
  - sentence-transformers: converte texto em numeros (embeddings)
  - FAISS: busca os vetores mais similares de forma eficiente
  - pdfplumber + PyMuPDF: leitura dos PDFs do corpus
  - deep-translator: traducao automatica ingles -> portugues (requer internet)
"""

import numpy as np                          # manipulacao de arrays numericos
import faiss                                # busca por similaridade vetorial
from sentence_transformers import SentenceTransformer  # modelo de embeddings
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator

from documents import carregar_documentos   # carrega e processa os PDFs do corpus

# Modelo multilingual — entende portugues, ingles e mais de 50 outros idiomas
# Tamanho: ~420MB, baixado automaticamente na primeira execucao
MODELO = "paraphrase-multilingual-mpnet-base-v2"

# Busca os 6 paragrafos mais proximos e filtra para exibir os 3 melhores de artigos distintos
# Buscar mais do que o necessario garante diversidade nos resultados finais
TOP_K = 6


def detectar_idioma(texto: str) -> str:
    """
    Detecta o idioma de um texto e retorna o codigo ISO ('pt', 'en', etc.).
    Retorna 'desconhecido' se nao for possivel detectar (texto muito curto, por exemplo).
    """
    try:
        return detect(texto)
    except LangDetectException:
        return "desconhecido"


def traduzir_se_necessario(trecho: str, idioma_pergunta: str) -> tuple[str, bool]:
    """
    Traduz o trecho de ingles para portugues se a pergunta foi feita em portugues.

    Retorna uma tupla com:
      - o texto (traduzido ou original)
      - um booleano indicando se a traducao foi feita

    Se nao houver internet ou a traducao falhar, retorna o texto original sem erro.
    Isso garante que o sistema nunca quebre por causa da traducao.
    """
    idioma_trecho = detectar_idioma(trecho)

    # So traduz se a pergunta for em portugues e o trecho estiver em ingles
    if idioma_pergunta == "pt" and idioma_trecho == "en":
        try:
            traduzido = GoogleTranslator(source="en", target="pt").translate(trecho[:500])
            return traduzido, True
        except Exception:
            # Se a traducao falhar (sem internet, limite atingido, etc.), exibe o original
            return trecho, False

    return trecho, False


def construir_indice(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """
    Cria o indice FAISS a partir dos embeddings do corpus.

    O IndexFlatL2 calcula a distancia euclidiana entre vetores — quanto menor
    a distancia, mais parecidos sao os textos semanticamente.
    Nao usa aproximacoes: compara com todos os vetores do corpus (busca exata).
    """
    dimensao = embeddings.shape[1]  # numero de dimensoes de cada vetor (768 neste modelo)
    indice = faiss.IndexFlatL2(dimensao)
    indice.add(embeddings)          # adiciona todos os vetores ao indice
    return indice


def buscar(
    pergunta: str,
    modelo: SentenceTransformer,
    indice: faiss.IndexFlatL2,
    textos: list[str],
    metadados: list[dict],
    top_k: int = TOP_K,
) -> list[dict]:
    """
    Recebe uma pergunta em texto e retorna os paragrafos mais relevantes do corpus.

    Como funciona:
      1. Converte a pergunta em um vetor (embedding)
      2. Pede ao FAISS os top_k vetores mais proximos
      3. Monta a lista de resultados com texto e metadados de cada paragrafo
    """
    # Converter a pergunta no mesmo "idioma numerico" dos documentos
    embedding_pergunta = modelo.encode([pergunta], convert_to_numpy=True)

    # Buscar no indice: retorna distancias e indices dos paragrafos mais proximos
    distancias, indices = indice.search(embedding_pergunta, top_k)

    resultados = []
    for i, idx in enumerate(indices[0]):
        resultados.append({
            "posicao": i + 1,
            "distancia": float(distancias[0][i]),  # menor = mais relevante
            "texto": textos[idx],
            "titulo": metadados[idx]["titulo"],
            "autores": metadados[idx]["autores"],
            "publicacao": metadados[idx]["publicacao"],
        })
    return resultados


def exibir_resultado(resultado: dict, idioma_pergunta: str) -> None:
    """
    Formata e imprime um resultado de busca no terminal.
    Se a pergunta foi em portugues e o trecho em ingles, exibe a traducao.
    """
    print(f"\n  [{resultado['posicao']}] {resultado['titulo']}")
    print(f"      Autores: {resultado['autores']}")
    print(f"      Publicacao: {resultado['publicacao']}")

    trecho, foi_traduzido = traduzir_se_necessario(resultado["texto"][:500], idioma_pergunta)

    if foi_traduzido:
        # Indica ao usuario que o trecho foi traduzido automaticamente
        print(f"      Trecho (traduzido): \"{trecho[:400]}\"")
    else:
        print(f"      Trecho: \"{resultado['texto'][:400]}\"")


def main():
    print("=" * 60)
    print("  Q3 — Busca Semantica com Embeddings")
    print("=" * 60)

    # ETAPA 1: Carregar e processar os PDFs do corpus
    print("\n[1/3] Carregando documentos do corpus...")
    textos, metadados = carregar_documentos()

    # ETAPA 2: Gerar embeddings e montar o indice de busca
    # Esta etapa pode levar alguns segundos na primeira execucao
    # (o modelo tambem e baixado aqui se nao estiver em cache)
    print("[2/3] Gerando embeddings (pode demorar alguns segundos)...")
    modelo = SentenceTransformer(MODELO)
    embeddings = modelo.encode(textos, convert_to_numpy=True, show_progress_bar=True)
    indice = construir_indice(embeddings)
    print(f"      Indice criado com {indice.ntotal} vetores.\n")

    # ETAPA 3: Loop interativo de busca
    print("[3/3] Sistema pronto! Digite sua pergunta ou 'sair' para encerrar.\n")
    print("-" * 60)

    while True:
        pergunta = input("\nPergunta: ").strip()

        # ignora linha vazia — aguarda nova entrada
        if not pergunta:
            continue

        # encerra o programa se o usuario digitar 'sair'
        if pergunta.lower() == "sair":
            print("\nEncerrando. Ate logo!")
            break

        # Detectar idioma da pergunta para acionar a traducao quando necessario
        idioma_pergunta = detectar_idioma(pergunta)

        # Buscar os paragrafos mais relevantes
        resultados = buscar(pergunta, modelo, indice, textos, metadados)

        print(f"\n  Resultados mais relevantes para: \"{pergunta}\"")

        # Filtro de diversidade: exibe no maximo um resultado por artigo
        # Evita que a mesma fonte domine todos os resultados para uma pergunta
        vistos = set()
        for r in resultados:
            if r["titulo"] not in vistos or len(vistos) == len(resultados):
                exibir_resultado(r, idioma_pergunta)
                vistos.add(r["titulo"])

        print("\n" + "-" * 60)


if __name__ == "__main__":
    main()
