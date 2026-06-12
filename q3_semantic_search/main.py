"""
Q3 — Busca Semantica com Embeddings e FAISS

Como funciona (analogia simples):
  Imagine que cada trecho de texto vira um ponto num mapa gigante.
  Textos com significado parecido ficam proximos no mapa.
  Quando voce faz uma pergunta, ela tambem vira um ponto —
  e o sistema encontra os pontos mais proximos a ela.

Stack:
  - sentence-transformers: converte texto em numeros (embeddings)
  - FAISS: busca os embeddings mais similares de forma eficiente
  - pdfplumber: le os PDFs do corpus
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from documents import carregar_documentos

# Modelo multilingual otimizado para similaridade semantica em varios idiomas (~420MB)
# Ideal para corpus misto portugues/ingles como este projeto
MODELO = "paraphrase-multilingual-mpnet-base-v2"

# Busca os 6 mais proximos e filtra para exibir os 3 melhores de artigos distintos
TOP_K = 6


def construir_indice(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """
    Cria o indice FAISS com os embeddings do corpus.
    IndexFlatL2 faz busca por distancia euclidiana — sem aproximacoes.
    """
    dimensao = embeddings.shape[1]
    indice = faiss.IndexFlatL2(dimensao)
    indice.add(embeddings)
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
    Recebe uma pergunta, converte em embedding e busca os trechos mais relevantes.
    Retorna uma lista com os top_k resultados, cada um contendo texto e metadados.
    """
    embedding_pergunta = modelo.encode([pergunta], convert_to_numpy=True)
    distancias, indices = indice.search(embedding_pergunta, top_k)

    resultados = []
    for i, idx in enumerate(indices[0]):
        resultados.append({
            "posicao": i + 1,
            "distancia": float(distancias[0][i]),
            "texto": textos[idx],
            "titulo": metadados[idx]["titulo"],
            "autores": metadados[idx]["autores"],
            "publicacao": metadados[idx]["publicacao"],
        })
    return resultados


def exibir_resultado(resultado: dict) -> None:
    """Formata e imprime um resultado de busca."""
    print(f"\n  [{resultado['posicao']}] {resultado['titulo']}")
    print(f"      Autores: {resultado['autores']}")
    print(f"      Publicacao: {resultado['publicacao']}")
    print(f"      Trecho: \"{resultado['texto'][:400]}\"")


def main():
    print("=" * 60)
    print("  Q3 — Busca Semantica com Embeddings")
    print("=" * 60)

    # 1. Carregar corpus dos PDFs
    print("\n[1/3] Carregando documentos do corpus...")
    textos, metadados = carregar_documentos()

    # 2. Gerar embeddings e construir indice
    print("[2/3] Gerando embeddings (pode demorar alguns segundos)...")
    modelo = SentenceTransformer(MODELO)
    embeddings = modelo.encode(textos, convert_to_numpy=True, show_progress_bar=True)
    indice = construir_indice(embeddings)
    print(f"      Indice criado com {indice.ntotal} vetores.\n")

    # 3. Loop de busca interativo
    print("[3/3] Sistema pronto! Digite sua pergunta ou 'sair' para encerrar.\n")
    print("-" * 60)

    while True:
        pergunta = input("\nPergunta: ").strip()

        if not pergunta:
            continue

        if pergunta.lower() == "sair":
            print("\nEncerrando. Ate logo!")
            break

        resultados = buscar(pergunta, modelo, indice, textos, metadados)

        print(f"\n  Resultados mais relevantes para: \"{pergunta}\"")
        vistos = set()
        for r in resultados:
            # Evita exibir dois trechos do mesmo artigo seguidos
            if r["titulo"] not in vistos or len(vistos) == len(resultados):
                exibir_resultado(r)
                vistos.add(r["titulo"])

        print("\n" + "-" * 60)


if __name__ == "__main__":
    main()
