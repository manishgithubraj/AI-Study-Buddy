"""
Study Buddy RAG Engine
Handles PDF ingestion, text chunking, TF-IDF indexing,
and semantic search over uploaded study material.
"""

import re
import math
import json
from collections import Counter


def tokenize(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return [t for t in text.split() if len(t) > 2]


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks of ~chunk_size words."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk.strip())
        i += chunk_size - overlap
    return chunks


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from a Streamlit uploaded PDF file."""
    try:
        import PyPDF2
        import io
        reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def extract_text_from_txt(uploaded_file) -> str:
    """Extract text from a plain text file."""
    return uploaded_file.read().decode("utf-8", errors="ignore")


class StudyRAG:
    def __init__(self):
        self.chunks: list[str] = []
        self.chunk_tokens: list[list[str]] = []
        self.idf: dict[str, float] = {}
        self.doc_name: str = ""

    def is_loaded(self) -> bool:
        return len(self.chunks) > 0

    def load_document(self, text: str, doc_name: str = "document") -> int:
        """Chunk and index a document. Returns number of chunks."""
        self.doc_name = doc_name
        self.chunks = chunk_text(text)
        self.chunk_tokens = [tokenize(c) for c in self.chunks]
        self.idf = self._compute_idf()
        return len(self.chunks)

    def _compute_idf(self) -> dict[str, float]:
        N = len(self.chunk_tokens)
        df: dict[str, int] = {}
        for tokens in self.chunk_tokens:
            for t in set(tokens):
                df[t] = df.get(t, 0) + 1
        return {t: math.log((N + 1) / (freq + 1)) + 1 for t, freq in df.items()}

    def _tfidf(self, tokens: list[str]) -> dict[str, float]:
        tf = Counter(tokens)
        total = len(tokens) or 1
        return {t: (count / total) * self.idf.get(t, 1.0) for t, count in tf.items()}

    def _cosine(self, a: dict, b: dict) -> float:
        keys = set(a) & set(b)
        dot = sum(a[k] * b[k] for k in keys)
        ma = math.sqrt(sum(v * v for v in a.values()))
        mb = math.sqrt(sum(v * v for v in b.values()))
        return dot / (ma * mb) if ma and mb else 0.0

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        """Return top_k most relevant chunks for a query."""
        if not self.chunks:
            return []
        qvec = self._tfidf(tokenize(query))
        scores = []
        for i, tokens in enumerate(self.chunk_tokens):
            dvec = self._tfidf(tokens)
            scores.append((self._cosine(qvec, dvec), i))
        scores.sort(reverse=True)
        results = []
        for score, idx in scores[:top_k]:
            if score > 0.005:
                results.append({
                    "text": self.chunks[idx],
                    "score": round(score, 4),
                    "chunk_id": idx
                })
        return results

    def get_full_context(self, top_k: int = 8) -> str:
        """Get a broad overview of the document for summarization."""
        step = max(1, len(self.chunks) // top_k)
        sampled = [self.chunks[i] for i in range(0, len(self.chunks), step)][:top_k]
        return "\n\n".join(sampled)

    def format_context(self, results: list[dict]) -> str:
        if not results:
            return "No relevant content found."
        parts = []
        for i, r in enumerate(results):
            parts.append(f"[Excerpt {i+1}]\n{r['text']}")
        return "\n\n".join(parts)
