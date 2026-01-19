from nomic import embed as nomic_embed

def embed(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings using Nomic local embedding model (no API key).
    """
    result = nomic_embed.text(
        texts=texts,
        model="nomic-embed-text-v1.5",
        inference_mode="local"
    )
    return result["embeddings"]
