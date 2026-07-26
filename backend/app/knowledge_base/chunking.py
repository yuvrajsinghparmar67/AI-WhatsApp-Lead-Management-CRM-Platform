"""
Splits long text into overlapping chunks for embedding - the same
approach used everywhere for RAG: smaller, topically-focused units make
semantic search precise, and the overlap keeps a fact from being cut in
half across a chunk boundary.
"""


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    text = text.strip()
    if len(text) <= chunk_size:
        return [text] if text else []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = end - overlap

    return chunks
