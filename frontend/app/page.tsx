"use client";
import { useState } from "react";
import { ingest, query } from "../lib/api";

export default function Home() {
  const [text, setText] = useState<string>("");
  const [q, setQ] = useState<string>("");
  const [res, setRes] = useState<any>(null);
  const [file, setFile] = useState<File | null>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target?.result as string;
        setText(content);
      };
      reader.readAsText(selectedFile);
    }
  };

  return (
    <main style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Mini RAG</h1>

      <div style={{ marginBottom: "20px" }}>
        <h2>Ingest Text</h2>
        <input
          type="file"
          accept=".txt"
          onChange={handleFileUpload}
          style={{ marginBottom: "10px" }}
        />
        <br />
        <textarea
          placeholder="Paste text to ingest or upload a file"
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={10}
          cols={80}
          style={{ width: "100%", marginBottom: "10px" }}
        />
        <button onClick={async () => await ingest(text)}>Ingest</button>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <h2>Query</h2>
        <input
          placeholder="Ask a question"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
        />
        <button onClick={async () => setRes(await query(q))}>Ask</button>
      </div>

      {res && (
        <div>
          <h3>Answer</h3>
          <p>{res.answer}</p>
          <h4>Sources</h4>
          <ul>
            {res.citations.map((c: string, i: number) => (
              <li key={i}>[{i + 1}] {c}</li>
            ))}
          </ul>
          <h4>Token Usage</h4>
          <ul>
            <li>Retrieval Context Tokens: {res.tokens.retrieval_context_tokens}</li>
            <li>Prompt Tokens: {res.tokens.prompt_tokens}</li>
            <li>Estimated Completion Tokens: {res.tokens.estimated_completion_tokens}</li>
            <li>Estimated Total Tokens: {res.tokens.estimated_total_tokens}</li>
          </ul>
          <h4>Estimated Cost</h4>
          <p>${res.estimated_cost_usd} USD</p>
          <small>Latency: {res.latency_ms}ms</small>
        </div>
      )}
    </main>
  );
}
