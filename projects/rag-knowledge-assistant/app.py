"""Local RAG-style knowledge assistant using only the Python standard library.

Indexes .txt/.md files, ranks chunks with TF-IDF cosine similarity, and returns
source-grounded passages. An LLM can be added later for answer synthesis.
"""
from __future__ import annotations

import argparse
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

TOKEN_RE = re.compile(r"[a-zA-Z0-9_'-]+")

@dataclass
class Chunk:
    source: str
    text: str
    tf: Counter


def tokens(text: str) -> list[str]:
    return [x.lower() for x in TOKEN_RE.findall(text) if len(x) > 2]


def chunk_text(text: str, size: int = 120, overlap: int = 25) -> list[str]:
    words = text.split()
    step = max(1, size - overlap)
    return [" ".join(words[i:i + size]) for i in range(0, len(words), step) if words[i:i + size]]


def load_corpus(folder: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(folder.rglob("*")):
        if path.suffix.lower() not in {".txt", ".md"} or not path.is_file():
            continue
        for part in chunk_text(path.read_text(encoding="utf-8")):
            chunks.append(Chunk(str(path), part, Counter(tokens(part))))
    return chunks


def idf(chunks: list[Chunk]) -> dict[str, float]:
    n = len(chunks)
    df = Counter(term for c in chunks for term in c.tf)
    return {term: math.log((n + 1) / (freq + 1)) + 1 for term, freq in df.items()}


def vector(tf: Counter, weights: dict[str, float]) -> dict[str, float]:
    total = sum(tf.values()) or 1
    return {term: (count / total) * weights.get(term, 0.0) for term, count in tf.items()}


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    dot = sum(value * b.get(term, 0.0) for term, value in a.items())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def search(chunks: list[Chunk], query: str, k: int = 3):
    weights = idf(chunks)
    qv = vector(Counter(tokens(query)), weights)
    ranked = [(cosine(qv, vector(c.tf, weights)), c) for c in chunks]
    return sorted(ranked, key=lambda x: x[0], reverse=True)[:k]


def main() -> None:
    parser = argparse.ArgumentParser(description="Search a local knowledge base with TF-IDF retrieval.")
    parser.add_argument("query")
    parser.add_argument("--docs", default="sample_docs")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    corpus = load_corpus(Path(args.docs))
    if not corpus:
        raise SystemExit("No .txt or .md documents found.")
    print(f"Indexed {len(corpus)} chunks.\n")
    for rank, (score, chunk) in enumerate(search(corpus, args.query, args.top_k), 1):
        print(f"[{rank}] score={score:.3f} source={chunk.source}")
        print(chunk.text[:700], "\n")

if __name__ == "__main__":
    main()
