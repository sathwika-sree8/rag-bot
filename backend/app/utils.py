import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def chunk_text(text: str, size: int = 1000, overlap: int = 150):
    tokens = enc.encode(text)
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(tokens):
        end = start + size
        chunk_tokens = tokens[start:end]
        chunk_text = enc.decode(chunk_tokens)

        chunks.append({
            "chunk_index": chunk_index,
            "content": chunk_text,
            "token_count": len(chunk_tokens)
        })

        start += size - overlap
        chunk_index += 1

    return chunks
