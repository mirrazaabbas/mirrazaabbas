# RAG Knowledge Assistant

A dependency-free retrieval project that demonstrates the core retrieval layer behind Retrieval-Augmented Generation (RAG). It indexes local Markdown/text documents, splits them into overlapping chunks, calculates TF-IDF weights, ranks passages with cosine similarity, and returns source-grounded context.

## Why this project matters

Modern AI assistants need more than prompting: they need a way to retrieve relevant knowledge before generating an answer. This project implements that retrieval pipeline from first principles so the ranking logic is transparent and easy to extend.

## Architecture

`Documents → Chunking → Tokenization → TF-IDF Index → Query Vector → Cosine Ranking → Grounded Context`

## Features

- Recursive `.md` / `.txt` document ingestion
- Overlapping chunk generation
- TF-IDF weighting built from scratch
- Cosine-similarity semantic-style ranking
- Top-k source attribution
- Zero external dependencies
- Clean extension point for Gemini/OpenAI/local-model answer synthesis

## Run

```bash
python app.py "How can an AI assistant reduce hallucinations?" --docs sample_docs --top-k 3
```

## Engineering extensions

- Replace sparse TF-IDF vectors with embeddings
- Add a vector database such as FAISS/Chroma
- Add reranking
- Add conversational memory
- Connect an LLM for cited answer generation
- Add evaluation metrics for retrieval quality

## Skills demonstrated

Python · Information Retrieval · RAG · NLP · TF-IDF · Cosine Similarity · AI Architecture
