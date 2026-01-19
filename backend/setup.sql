-- Create the documents table with vector column
CREATE TABLE documents (
  id BIGSERIAL PRIMARY KEY,
  content TEXT,
  embedding VECTOR(768), -- Nomic embeddings are 768-dimensional
  source TEXT,
  title TEXT,
  section TEXT,
  chunk_index INTEGER
);

-- Create the match_documents function for similarity search
CREATE OR REPLACE FUNCTION match_documents(query_embedding VECTOR(768), match_count INT)
RETURNS TABLE(id BIGINT, content TEXT, similarity FLOAT)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT d.id, d.content, 1 - (d.embedding <=> query_embedding) AS similarity
  FROM documents d
  ORDER BY d.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- Enable pgvector extension if not already enabled
CREATE EXTENSION IF NOT EXISTS vector;
