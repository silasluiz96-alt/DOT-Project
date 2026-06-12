# Q3 — Busca Semântica com Embeddings

Sistema de busca semântica sobre um corpus de 5 artigos científicos reais,
usando **Sentence Transformers** para gerar embeddings e **FAISS** para busca eficiente.

## Evidências

📄 [Documento de evidências — evidencias_q3.pdf](../docs/evidencias_q3.pdf)

## Como funciona

> **Analogia:** Imagine que cada trecho de texto vira um ponto num mapa gigante.
> Textos com significado parecido ficam próximos nesse mapa.
> Quando você digita uma pergunta, ela também vira um ponto —
> e o sistema encontra os pontos mais próximos a ela.

1. Os 5 PDFs são lidos e divididos em trechos de ~500 caracteres
2. Cada trecho é convertido em um vetor de números (embedding) pelo modelo `paraphrase-multilingual-mpnet-base-v2`
3. O FAISS indexa todos esses vetores para busca ultrarrápida
4. A pergunta do usuário também vira um embedding
5. O sistema retorna os 3 trechos mais semanticamente similares

## Corpus de documentos

| Arquivo | Artigo | Autores | Publicação |
|---------|--------|---------|------------|
| `inovacao_aberta.pdf` | Inovação aberta nas estratégias competitivas das empresas brasileiras | Claudio Pitassi | REBRAE, 2014 |
| `ia_relacoes_trabalho.pdf` | IA e Inovação Tecnológica: Impactos nas Relações de Trabalho | Claudio Teixeira Damilano | UFSM, 2019 |
| `ia_generativa_mercado.pdf` | Adoção de IA Generativa em Inteligência e Pesquisa de Mercado | Madeira & Senise | USP / ABRAPCORP, 2025 |
| `digital_transformation.pdf` | Understanding digital transformation: A review and a research agenda | Gregory Vial | Journal of Strategic IS, 2019 |
| `machine_failure.pdf` | Integration of Data Analytics and Data Mining for Machine Failure Mitigation | Silas Luiz Bomfim et al. | Logistics / MDPI, 2025 |

## Como rodar

### 1. Instale as dependências

```bash
cd q3_semantic_search
pip install -r requirements.txt
```

> Na primeira execução, o modelo `paraphrase-multilingual-mpnet-base-v2` (~420MB) é baixado automaticamente. O modelo é multilíngue — entende português, inglês e mais de 50 idiomas.

### 2. Execute o sistema

```bash
python main.py
```

### 3. Faça suas perguntas

```
============================================================
  Q3 — Busca Semântica com Embeddings
============================================================

[1/3] Carregando documentos do corpus...
[2/3] Gerando embeddings...
[3/3] Sistema pronto! Digite sua pergunta ou 'sair' para encerrar.

Pergunta: Como a inteligência artificial impacta o mercado de trabalho?

  Resultados mais relevantes:
  [1] IA e Inovação Tecnológica: Impactos nas Relações de Trabalho
      Autores: Claudio Teixeira Damilano
      Trecho: ...a automação de tarefas cognitivas e o deslocamento de trabalhadores...
```

## Requisitos

- Python 3.10+
- Sem necessidade de API key (modelo roda localmente)
- Os PDFs estão incluídos na pasta `pdfs/`
