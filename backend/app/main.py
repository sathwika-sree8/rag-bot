from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .schemas import IngestRequest, QueryRequest
from .rag import ingest_text, answer_query

load_dotenv()

app = FastAPI(title="Mini RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ingest")
def ingest(req: IngestRequest):
    return ingest_text(req)

@app.post("/query")
def query(req: QueryRequest):
    return answer_query(req)
