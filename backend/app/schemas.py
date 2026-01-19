from pydantic import BaseModel

class IngestRequest(BaseModel):
    text: str
    source: str = "user_upload"
    title: str = "Untitled"

class QueryRequest(BaseModel):
    query: str
