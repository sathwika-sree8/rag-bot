import os
import cohere

co = cohere.Client(os.environ["COHERE_API_KEY"])

def rerank(query: str, documents_or_chunks, top_n: int = 5):
    if isinstance(documents_or_chunks[0], dict):
        # It's chunks: list[dict]
        documents = [c["content"] for c in documents_or_chunks]
        results = co.rerank(
            model="rerank-english-v3.0",
            query=query,
            documents=documents,
            top_n=top_n
        )
        reranked_chunks = []
        for r in results.results:
            reranked_chunks.append(documents_or_chunks[r.index])
        return reranked_chunks
    else:
        # It's documents: list[str]
        results = co.rerank(
            model="rerank-english-v3.0",
            query=query,
            documents=documents_or_chunks,
            top_n=top_n
        )
        return [documents_or_chunks[r.index] for r in results.results]
