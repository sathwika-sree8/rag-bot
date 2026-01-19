import time, os
from .db import supabase
from .embeddings import embed
from .utils import chunk_text
from .reranker import rerank
from .utils import enc
from groq import Groq

groq = Groq(api_key=os.environ["GROQ_API_KEY"])

def build_prompt(query: str, chunks: list[dict]) -> str:
    context = ""
    for i, c in enumerate(chunks):
        context += f"[{i+1}] {c['content']}\n\n"

    return f"""
Answer the question using ONLY the context below.
If the answer is not present, say:
"I don’t have enough information to answer that."

Context:
{context}

Question: {query}
"""
def generate_answer(query: str, reranked_chunks: list[dict]) -> str:
    prompt = build_prompt(query, reranked_chunks)

    completion = groq.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return completion.choices[0].message.content, prompt

def ingest_text(req):
    chunks = chunk_text(req.text)
    contents = [c["content"] for c in chunks]
    total_tokens = sum(c["token_count"] for c in chunks)
    embeddings = embed([c["content"] for c in chunks])

    rows = []
    for chunk, emb in zip(chunks, embeddings):
        rows.append({
            "content": chunk["content"],
            "embedding": emb,
            "source": req.source,
            "title": req.title,
            "section": "body",
            "chunk_index": chunk["chunk_index"]
        })
    supabase.table("documents").delete().eq("source", req.source).execute()
    supabase.table("documents").insert(rows).execute()

    return {
        "chunks_ingested": len(rows),
        "tokens_processed": total_tokens
    }

def retrieve_chunks(query: str, top_k: int = 8):
    query_embedding = embed([query])[0]

    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": top_k
        }
    ).execute()

    return response.data or []

def answer_query(req):
    start = time.time()

    # 1. Embed query
    q_emb = embed([req.query])[0]

    # 2. Retrieve top-k chunks
    res = supabase.rpc(
        "match_documents",
        {
            "query_embedding": q_emb,
            "match_count": 8
        }
    ).execute()

    if not res.data:
        return {
            "answer": "I don’t have enough information to answer that.",
            "citations": [],
            "tokens": {},
            "latency_ms": int((time.time() - start) * 1000)
        }

    retrieved_chunks = res.data
    print("RETRIEVED:", retrieved_chunks)
    # 3. Rerank chunks
    reranked_chunks = rerank(req.query, retrieved_chunks, top_n=5)

    # 4. Generate answer
    answer, prompt = generate_answer(req.query, reranked_chunks)

    # 5. Build citations
    citations = [c["content"][:200] for c in reranked_chunks]

    # 6. Count tokens
    retrieval_context_tokens = sum(len(enc.encode(c["content"])) for c in retrieved_chunks)
    prompt_tokens = len(enc.encode(prompt))
    estimated_completion_tokens = 300
    estimated_total_tokens = prompt_tokens + estimated_completion_tokens

    # 7. Rough cost estimate (example: $0.01 per 1000 tokens for LLM, $0.002 per doc for rerank)
    llm_cost = (estimated_total_tokens / 1000) * 0.01
    rerank_cost = len(reranked_chunks) * 0.002
    total_cost = llm_cost + rerank_cost

    # 8. Return everything
    return {
        "answer": answer,
        "citations": citations,
        "tokens": {
            "retrieval_context_tokens": retrieval_context_tokens,
            "prompt_tokens": prompt_tokens,
            "estimated_completion_tokens": estimated_completion_tokens,
            "estimated_total_tokens": estimated_total_tokens
        },
        "estimated_cost_usd": round(total_cost, 4),
        "latency_ms": int((time.time() - start) * 1000)
    }
